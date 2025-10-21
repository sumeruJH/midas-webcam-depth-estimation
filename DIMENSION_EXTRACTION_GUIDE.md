# Building Dimension Extraction Guide

## Overview

This guide explains how to use the building dimension extraction feature to extract accurate measurements from building images using depth maps and GPT-4.

## Workflow

The complete workflow consists of the following steps:

```
Input Image → Parallax Correction → Depth Map Generation → Dimension Extraction → GPT-4 Analysis → JSON Output
```

### Step 1: Parallax Correction

Before processing, images are corrected for:
- **Lens distortion**: Corrects barrel/pincushion distortion from camera lenses
- **Perspective distortion**: Adjusts for viewing angle effects

This ensures accurate measurements by removing optical artifacts.

### Step 2: Depth Map Generation

The MiDaS model generates a depth map where:
- Darker areas = closer to camera
- Lighter areas = farther from camera

The depth map provides 3D spatial information crucial for accurate dimension estimation.

### Step 3: Dimension Extraction

The automated extraction module:
1. Detects building edges and contours
2. Analyzes depth information
3. Calculates dimensions in meters:
   - Width (horizontal span)
   - Height (vertical extent)
   - Depth (front-to-back)
   - Floor area (square meters)
   - Volume (cubic meters)
4. Provides confidence scores

### Step 4: GPT-4 Analysis

The generated prompt guides GPT-4 to:
- Validate automated measurements
- Provide refined estimates using visual cues
- Account for architectural details
- Handle complex structures
- Identify uncertainties and limitations

### Step 5: JSON Output

All results are saved in structured JSON format for easy integration with other systems.

## Usage Examples

### Basic Usage

Process a single building image:

```bash
python extract_building_dimensions.py building.jpg
```

This will create:
- `output/building_corrected.jpg` - Parallax-corrected image
- `output/building_depth.jpg` - Colored depth map
- `output/building_dimensions.json` - Extracted dimensions
- `output/building_gpt4_prompt.txt` - GPT-4 analysis prompt

### Batch Processing

Process multiple buildings at once:

```bash
python extract_building_dimensions.py building1.jpg building2.jpg building3.jpg
```

Results for all buildings will be saved individually, plus:
- `output/all_dimensions.json` - Combined results for all buildings

### Advanced Options

```bash
# Skip parallax correction (if already corrected)
python extract_building_dimensions.py building.jpg --no-parallax-correction

# Specify custom output directory
python extract_building_dimensions.py building.jpg --output-dir my_results

# View the GPT-4 prompt template
python extract_building_dimensions.py --show-prompt
```

## Output Format

### Dimensions JSON Structure

```json
{
  "width_meters": 25.5,
  "height_meters": 18.2,
  "depth_meters": 12.3,
  "area_square_meters": 464.1,
  "volume_cubic_meters": 5708.43,
  "confidence": 0.85,
  "metadata": {
    "bounding_box": {
      "x": 120,
      "y": 80,
      "width": 640,
      "height": 480
    },
    "depth_statistics": {
      "average": 0.654,
      "min": 0.423,
      "max": 0.891
    },
    "scale_factor": 10.0
  }
}
```

### Batch Processing Output

```json
{
  "total_buildings": 3,
  "buildings": [
    {
      "image_path": "building1.jpg",
      "corrected_image_path": "output/building1_corrected.jpg",
      "depth_map_path": "output/building1_depth.jpg",
      "dimensions": { ... },
      "gpt4_prompt_path": "output/building1_gpt4_prompt.txt"
    },
    ...
  ]
}
```

## GPT-4 Prompt Usage

### What the Prompt Does

The generated GPT-4 prompt includes:

1. **Context and Instructions**: Detailed guidelines for analyzing building images
2. **Required Measurements**: Specifications for width, height, depth, area, volume
3. **Analysis Steps**: Step-by-step methodology
4. **Output Format**: Structured JSON schema
5. **Edge Cases**: Handling various building types and perspectives
6. **Quality Indicators**: Confidence scoring guidelines

### How to Use the Prompt

1. **Get the Prompt**:
   ```bash
   python extract_building_dimensions.py building.jpg
   # The prompt is saved to: output/building_gpt4_prompt.txt
   ```

2. **Send to GPT-4**:
   - Copy the prompt text
   - Attach the corrected image and depth map
   - Send to GPT-4 (via API or ChatGPT interface)

3. **Receive Analysis**:
   - GPT-4 will return detailed measurements in JSON format
   - Includes confidence scores and analysis notes
   - Can identify limitations and uncertainties

### Example GPT-4 Response

```json
{
  "building_id": "building_001",
  "dimensions": {
    "width_meters": 24.8,
    "height_meters": 19.1,
    "depth_meters": 13.2,
    "floor_area_sqm": 473.68,
    "volume_cubic_m": 6252.576
  },
  "confidence_scores": {
    "width": 0.88,
    "height": 0.82,
    "depth": 0.65,
    "overall": 0.78
  },
  "structural_details": {
    "num_floors": 5,
    "num_visible_windows": 24,
    "roof_type": "flat",
    "architectural_style": "modern commercial"
  },
  "measurement_method": {
    "reference_used": "standard window height (1.5m)",
    "assumptions": [
      "Each floor is approximately 3.5 meters high",
      "Building has rectangular footprint"
    ],
    "limitations": [
      "Right side partially occluded by tree",
      "Depth measurement has higher uncertainty"
    ]
  },
  "depth_analysis": {
    "min_depth": 0.42,
    "max_depth": 0.89,
    "avg_depth": 0.65,
    "depth_variance": 0.12
  },
  "notes": "Building appears to be a modern commercial structure with regular window patterns. Measurement confidence is high for width and height due to clear boundaries. Depth has moderate confidence due to limited depth variation visible in the depth map."
}
```

## Handling Different Scenarios

### Clear, Front-Facing Building
- **Best case scenario**
- High confidence measurements
- All dimensions reliable

### Angled View
- Use depth map heavily for depth estimation
- Width and height may need perspective adjustment
- GPT-4 prompt accounts for this

### Partially Occluded
- Automated extraction may have lower confidence
- GPT-4 can infer hidden portions
- Results include uncertainty notes

### Complex Structure (L-shaped, multiple wings)
- Automated extraction finds primary structure
- GPT-4 can break down into components
- May return ranges or multiple measurements

## Tips for Best Results

1. **Image Quality**:
   - Use high-resolution images (minimum 1920x1080)
   - Avoid motion blur and poor lighting
   - Capture entire building if possible

2. **Camera Position**:
   - Front-facing views work best
   - Minimize viewing angle (< 45° is ideal)
   - Include some ground reference if possible

3. **Reference Points**:
   - If known dimensions exist, include them in metadata
   - Windows, doors, and floors provide scale
   - Human figures can serve as size references

4. **Multiple Views**:
   - Process from different angles
   - Cross-reference measurements
   - Improves overall accuracy

## Limitations

### Automated Extraction
- Relative measurements (not absolute without calibration)
- Assumes single building dominates the image
- Limited by depth map accuracy
- May struggle with complex geometries

### Depth Maps
- Provide relative depth, not absolute distances
- Quality depends on MiDaS model and image quality
- Reflective surfaces may cause artifacts
- Transparent materials not handled well

### General
- Scale estimation assumes typical building proportions
- Accuracy improves with reference measurements
- Best for buildings < 50 meters from camera
- Weather conditions affect depth estimation

## Integration with Other Tools

### Python API

```python
from parallax_correction import auto_correct_image
from dimension_extraction import DimensionExtractor
import cv2

# Load and correct image
image = cv2.imread('building.jpg')
corrected = auto_correct_image(image)

# Extract dimensions (assuming you have a depth map)
extractor = DimensionExtractor(reference_distance=10.0)
dimensions = extractor.extract_dimensions(corrected, depth_map)

# Get JSON output
json_output = dimensions.to_json()
print(json_output)
```

### Custom GPT-4 Prompts

```python
from gpt4_prompts import generate_prompt_with_context

# Create custom prompt
prompt = generate_prompt_with_context(
    image_description="Modern office building, front view, clear sky",
    reference_measurements={"door_height": 2.1},
    building_type="commercial",
    special_instructions="Focus on window patterns for scaling"
)
```

## Troubleshooting

### Low Confidence Scores
- Image may be too distant or occluded
- Try processing from a different angle
- Provide reference measurements

### Inaccurate Depth Map
- Check image quality and lighting
- Avoid reflective surfaces in frame
- Consider using different MiDaS model

### Processing Errors
- Ensure all dependencies are installed
- Check image file format (JPEG, PNG supported)
- Verify sufficient disk space for output

## Support and Contributions

For issues, questions, or contributions, please refer to the main README or open an issue on the GitHub repository.
