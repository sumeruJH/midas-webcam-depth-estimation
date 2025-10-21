"""
Example: Building Dimension Extraction Demo

This script demonstrates the usage of the building dimension extraction modules
with example data and explains each step.
"""

import numpy as np
import cv2
import json

# Example 1: Using Parallax Correction
print("="*70)
print("EXAMPLE 1: Parallax Correction")
print("="*70)

from parallax_correction import correct_parallax, correct_perspective, auto_correct_image

print("""
Parallax correction removes distortions in images caused by:
1. Lens distortion (barrel/pincushion effects)
2. Perspective distortion (viewing angle effects)

This is essential for accurate dimensional measurements.
""")

# Simulate an image for demonstration
example_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

print("Example usage:")
print("""
import cv2
from parallax_correction import auto_correct_image

# Load your building image
image = cv2.imread('building.jpg')

# Apply automatic correction
corrected_image = auto_correct_image(image)

# Save corrected image
cv2.imwrite('building_corrected.jpg', corrected_image)
""")

# Example 2: Dimension Extraction
print("\n" + "="*70)
print("EXAMPLE 2: Dimension Extraction")
print("="*70)

from dimension_extraction import DimensionExtractor, BuildingDimensions

print("""
The DimensionExtractor analyzes images with depth maps to calculate:
- Width (horizontal span in meters)
- Height (vertical extent in meters)
- Depth (front-to-back dimension in meters)
- Floor area (square meters)
- Volume (cubic meters)
""")

print("Example usage:")
print("""
import cv2
from dimension_extraction import DimensionExtractor

# Load image and depth map
image = cv2.imread('building.jpg')
depth_map = cv2.imread('building_depth.jpg', cv2.IMREAD_GRAYSCALE)

# Create extractor
extractor = DimensionExtractor(reference_distance=10.0)

# Extract dimensions
dimensions = extractor.extract_dimensions(image, depth_map)

# Display results
print(f"Width: {dimensions.width_meters} m")
print(f"Height: {dimensions.height_meters} m")
print(f"Depth: {dimensions.depth_meters} m")
print(f"Area: {dimensions.area_square_meters} m²")
print(f"Volume: {dimensions.volume_cubic_meters} m³")
print(f"Confidence: {dimensions.confidence:.2%}")

# Save to JSON
with open('dimensions.json', 'w') as f:
    f.write(dimensions.to_json())
""")

# Demonstrate the BuildingDimensions data structure
print("\nExample BuildingDimensions object:")
example_dimensions = BuildingDimensions(
    width_meters=24.5,
    height_meters=18.3,
    depth_meters=12.7,
    area_square_meters=448.35,
    volume_cubic_meters=5693.845,
    confidence=0.87,
    metadata={
        "bounding_box": {"x": 100, "y": 50, "width": 500, "height": 400},
        "depth_statistics": {"average": 0.65, "min": 0.42, "max": 0.88},
        "scale_factor": 10.0
    }
)

print(example_dimensions.to_json())

# Example 3: GPT-4 Prompts
print("\n" + "="*70)
print("EXAMPLE 3: GPT-4 Prompts")
print("="*70)

from gpt4_prompts import (
    GPT4_DIMENSION_EXTRACTION_PROMPT,
    generate_prompt_with_context,
    format_results_for_gpt4
)

print("""
The GPT-4 prompt templates guide AI analysis of building images.
These prompts provide:
- Detailed instructions for measurement extraction
- Guidelines for handling various building types
- Output format specifications (JSON)
- Edge case handling strategies
""")

print("Example usage:")
print("""
from gpt4_prompts import generate_prompt_with_context

# Generate a custom prompt
prompt = generate_prompt_with_context(
    image_description="Modern commercial building, front view",
    reference_measurements={"door_height": 2.1, "window_height": 1.5},
    building_type="commercial",
    special_instructions="Use window patterns for height estimation"
)

# Use the prompt with GPT-4 (via API or ChatGPT)
# Attach the corrected image and depth map
# GPT-4 will return detailed analysis in JSON format
""")

print("\nGenerating example custom prompt...")
custom_prompt = generate_prompt_with_context(
    image_description="3-story residential building, slight angle view",
    reference_measurements={"known_door_height": 2.1},
    building_type="residential",
    special_instructions="Account for tree partially occluding right side"
)

print("\nCustom prompt preview (first 500 characters):")
print(custom_prompt[:500] + "...\n")

# Example 4: Complete Workflow
print("="*70)
print("EXAMPLE 4: Complete Workflow")
print("="*70)

print("""
The complete workflow integrates all modules:

1. Load building image
2. Apply parallax correction
3. Generate depth map (using MiDaS)
4. Extract dimensions automatically
5. Generate GPT-4 prompt for refinement
6. Output results in JSON format

Use the extract_building_dimensions.py script for the complete pipeline:
""")

print("""
# Command line usage:
python extract_building_dimensions.py building.jpg

# This will:
# - Correct the image for parallax
# - Generate a depth map
# - Extract dimensions
# - Create a GPT-4 prompt
# - Save all outputs to the output/ directory

# For multiple buildings:
python extract_building_dimensions.py building1.jpg building2.jpg building3.jpg

# View the GPT-4 prompt template:
python extract_building_dimensions.py --show-prompt
""")

# Example 5: JSON Output Format
print("\n" + "="*70)
print("EXAMPLE 5: JSON Output Format")
print("="*70)

print("""
All dimension data is output in structured JSON format for easy integration.
""")

example_output = {
    "width_meters": 25.3,
    "height_meters": 19.2,
    "depth_meters": 13.5,
    "area_square_meters": 485.76,
    "volume_cubic_meters": 6557.76,
    "confidence": 0.84,
    "metadata": {
        "bounding_box": {
            "x": 120,
            "y": 80,
            "width": 640,
            "height": 480
        },
        "depth_statistics": {
            "average": 0.67,
            "min": 0.45,
            "max": 0.89
        },
        "scale_factor": 10.0
    }
}

print("\nExample JSON output:")
print(json.dumps(example_output, indent=2))

# Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)

print("""
This building dimension extraction system provides:

✓ Parallax correction for accurate measurements
✓ Automated dimension extraction from depth maps
✓ GPT-4 integration for AI-assisted analysis
✓ JSON output format for easy integration
✓ Batch processing capabilities
✓ Confidence scoring and metadata

Key Files:
- parallax_correction.py    : Image correction functions
- dimension_extraction.py   : Dimension calculation logic
- gpt4_prompts.py          : GPT-4 prompt templates
- extract_building_dimensions.py : Complete pipeline script

Documentation:
- README.md                : Main project documentation
- DIMENSION_EXTRACTION_GUIDE.md : Detailed usage guide
- examples.py              : This file (usage examples)

For more information, see DIMENSION_EXTRACTION_GUIDE.md
""")

print("="*70)
print("END OF EXAMPLES")
print("="*70)
