"""
Building Dimension Extraction - Example Usage

This script demonstrates the complete workflow for extracting building dimensions
from images using the MiDaS depth estimation model, parallax correction, and
dimension extraction capabilities.
"""

import cv2
import torch
import numpy as np
import json
import argparse
from pathlib import Path
from PIL import Image
from torchvision.transforms import Compose, Resize, ToTensor, Normalize

from parallax_correction import auto_correct_image, correct_parallax
from dimension_extraction import DimensionExtractor, process_building_images
from gpt4_prompts import (
    GPT4_DIMENSION_EXTRACTION_PROMPT,
    generate_prompt_with_context,
    format_results_for_gpt4
)


def load_midas_model(model_type="DPT_Large"):
    """
    Load the MiDaS model for depth estimation.
    
    Args:
        model_type: Type of MiDaS model to load
    
    Returns:
        Tuple of (model, transform, device)
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Load MiDaS model
    midas = torch.hub.load("intel-isl/MiDaS", model_type)
    midas.to(device).eval()
    
    # Setup transforms
    transform = Compose([
        Resize((384, 384)),
        ToTensor(),
        Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    
    return midas, transform, device


def generate_depth_map(image_path: str, midas_model, transform, device):
    """
    Generate depth map for an image using MiDaS.
    
    Args:
        image_path: Path to input image
        midas_model: Loaded MiDaS model
        transform: Image transformation pipeline
        device: Torch device
    
    Returns:
        Depth map as numpy array
    """
    # Load image
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    
    # Transform and predict
    img_input = transform(img_pil).unsqueeze(0).to(device)
    
    with torch.no_grad():
        prediction = midas_model(img_input)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img_rgb.shape[:2],
            mode="bicubic",
            align_corners=False
        ).squeeze()
    
    depth_map = prediction.cpu().numpy()
    
    return depth_map


def process_single_image(
    image_path: str,
    output_dir: str = "output",
    apply_parallax_correction: bool = True,
    save_intermediate: bool = True
):
    """
    Complete processing pipeline for a single building image.
    
    Args:
        image_path: Path to input building image
        output_dir: Directory to save output files
        apply_parallax_correction: Whether to apply parallax correction
        save_intermediate: Whether to save intermediate processing results
    
    Returns:
        Dictionary containing all results
    """
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    image_name = Path(image_path).stem
    
    print(f"\n{'='*60}")
    print(f"Processing: {image_path}")
    print(f"{'='*60}")
    
    # Step 1: Load image
    print("\n[1/5] Loading image...")
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    # Step 2: Apply parallax correction
    if apply_parallax_correction:
        print("[2/5] Applying parallax correction...")
        corrected_image = auto_correct_image(image)
        
        if save_intermediate:
            corrected_path = output_path / f"{image_name}_corrected.jpg"
            cv2.imwrite(str(corrected_path), corrected_image)
            print(f"  Saved corrected image: {corrected_path}")
    else:
        print("[2/5] Skipping parallax correction...")
        corrected_image = image
    
    # Step 3: Generate depth map
    print("[3/5] Generating depth map with MiDaS...")
    midas, transform, device = load_midas_model()
    
    # Save corrected image temporarily for depth processing
    temp_path = output_path / f"{image_name}_temp.jpg"
    cv2.imwrite(str(temp_path), corrected_image)
    
    depth_map = generate_depth_map(str(temp_path), midas, transform, device)
    
    # Normalize and save depth map
    depth_normalized = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX)
    depth_colored = cv2.applyColorMap(depth_normalized.astype(np.uint8), cv2.COLORMAP_INFERNO)
    
    if save_intermediate:
        depth_path = output_path / f"{image_name}_depth.jpg"
        cv2.imwrite(str(depth_path), depth_colored)
        print(f"  Saved depth map: {depth_path}")
    
    # Clean up temp file
    temp_path.unlink()
    
    # Step 4: Extract dimensions
    print("[4/5] Extracting building dimensions...")
    extractor = DimensionExtractor()
    dimensions = extractor.extract_dimensions(corrected_image, depth_map)
    
    # Save dimensions to JSON
    dimensions_path = output_path / f"{image_name}_dimensions.json"
    with open(dimensions_path, 'w') as f:
        f.write(dimensions.to_json())
    print(f"  Saved dimensions: {dimensions_path}")
    
    # Step 5: Generate GPT-4 prompt
    print("[5/5] Generating GPT-4 prompt...")
    gpt4_prompt = format_results_for_gpt4(
        image_path=image_path,
        depth_map_path=str(output_path / f"{image_name}_depth.jpg"),
        metadata={
            "parallax_corrected": apply_parallax_correction,
            "extracted_dimensions": dimensions.to_dict()
        }
    )
    
    prompt_path = output_path / f"{image_name}_gpt4_prompt.txt"
    with open(prompt_path, 'w') as f:
        f.write(gpt4_prompt)
    print(f"  Saved GPT-4 prompt: {prompt_path}")
    
    # Prepare results summary
    results = {
        "image_path": image_path,
        "corrected_image_path": str(output_path / f"{image_name}_corrected.jpg") if apply_parallax_correction else None,
        "depth_map_path": str(output_path / f"{image_name}_depth.jpg"),
        "dimensions": dimensions.to_dict(),
        "gpt4_prompt_path": str(prompt_path)
    }
    
    print(f"\n{'='*60}")
    print("Processing complete!")
    print(f"{'='*60}")
    print("\nExtracted Dimensions:")
    print(f"  Width:  {dimensions.width_meters} m")
    print(f"  Height: {dimensions.height_meters} m")
    print(f"  Depth:  {dimensions.depth_meters} m")
    print(f"  Area:   {dimensions.area_square_meters} m²")
    print(f"  Volume: {dimensions.volume_cubic_meters} m³")
    print(f"  Confidence: {dimensions.confidence:.2%}")
    
    return results


def process_multiple_images(
    image_paths: list,
    output_dir: str = "output",
    apply_parallax_correction: bool = True
):
    """
    Process multiple building images in batch.
    
    Args:
        image_paths: List of paths to building images
        output_dir: Directory to save output files
        apply_parallax_correction: Whether to apply parallax correction
    
    Returns:
        List of results for all images
    """
    all_results = []
    
    for image_path in image_paths:
        try:
            results = process_single_image(
                image_path=image_path,
                output_dir=output_dir,
                apply_parallax_correction=apply_parallax_correction,
                save_intermediate=True
            )
            all_results.append(results)
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            continue
    
    # Save combined results
    output_path = Path(output_dir)
    combined_path = output_path / "all_dimensions.json"
    
    with open(combined_path, 'w') as f:
        json.dump({
            "total_buildings": len(all_results),
            "buildings": all_results
        }, f, indent=2)
    
    print(f"\n\nSaved combined results: {combined_path}")
    
    return all_results


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Extract building dimensions from images with depth estimation"
    )
    parser.add_argument(
        "images",
        nargs="+",
        help="Path(s) to building image(s)"
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Output directory for results (default: output)"
    )
    parser.add_argument(
        "--no-parallax-correction",
        action="store_true",
        help="Skip parallax correction step"
    )
    parser.add_argument(
        "--show-prompt",
        action="store_true",
        help="Display the GPT-4 prompt template"
    )
    
    args = parser.parse_args()
    
    if args.show_prompt:
        print("\n" + "="*60)
        print("GPT-4 Dimension Extraction Prompt")
        print("="*60)
        print(GPT4_DIMENSION_EXTRACTION_PROMPT)
        return
    
    # Process images
    if len(args.images) == 1:
        process_single_image(
            image_path=args.images[0],
            output_dir=args.output_dir,
            apply_parallax_correction=not args.no_parallax_correction
        )
    else:
        process_multiple_images(
            image_paths=args.images,
            output_dir=args.output_dir,
            apply_parallax_correction=not args.no_parallax_correction
        )


if __name__ == "__main__":
    main()
