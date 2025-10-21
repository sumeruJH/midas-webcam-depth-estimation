# Quick Reference: Building Dimension Extraction

## Installation

```bash
# Clone the repository
git clone https://github.com/sumeruJH/midas-webcam-depth-estimation.git
cd midas-webcam-depth-estimation

# Create conda environment
conda create -n midas-depth python=3.10 -y
conda activate midas-depth

# Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### Single Image Processing

```bash
python extract_building_dimensions.py building.jpg
```

**Output files (in `output/` directory):**
- `building_corrected.jpg` - Parallax-corrected image
- `building_depth.jpg` - Colored depth map
- `building_dimensions.json` - Extracted dimensions
- `building_gpt4_prompt.txt` - GPT-4 analysis prompt

### Multiple Images

```bash
python extract_building_dimensions.py img1.jpg img2.jpg img3.jpg
```

**Additional output:**
- `all_dimensions.json` - Combined results for all buildings

## Command Line Options

```bash
# Custom output directory
python extract_building_dimensions.py building.jpg --output-dir my_results

# Skip parallax correction
python extract_building_dimensions.py building.jpg --no-parallax-correction

# View GPT-4 prompt template
python extract_building_dimensions.py --show-prompt
```

## Python API Usage

### Basic Dimension Extraction

```python
import cv2
from parallax_correction import auto_correct_image
from dimension_extraction import DimensionExtractor

# Load and correct image
image = cv2.imread('building.jpg')
corrected = auto_correct_image(image)

# Assume you have a depth_map (from MiDaS or similar)
# depth_map = ...

# Extract dimensions
extractor = DimensionExtractor(reference_distance=10.0)
dimensions = extractor.extract_dimensions(corrected, depth_map)

# Access results
print(f"Width: {dimensions.width_meters} m")
print(f"Height: {dimensions.height_meters} m")
print(f"Depth: {dimensions.depth_meters} m")
print(f"Area: {dimensions.area_square_meters} m²")
print(f"Volume: {dimensions.volume_cubic_meters} m³")
print(f"Confidence: {dimensions.confidence:.2%}")

# Save to JSON
with open('output.json', 'w') as f:
    f.write(dimensions.to_json())
```

### Custom GPT-4 Prompts

```python
from gpt4_prompts import generate_prompt_with_context

prompt = generate_prompt_with_context(
    image_description="Modern office building, front view",
    reference_measurements={"door_height": 2.1},
    building_type="commercial",
    special_instructions="Use window patterns for scaling"
)

# Use this prompt with GPT-4 API or ChatGPT
```

### Batch Processing

```python
from dimension_extraction import process_building_images

image_paths = ['building1.jpg', 'building2.jpg', 'building3.jpg']
depth_paths = ['depth1.jpg', 'depth2.jpg', 'depth3.jpg']

results = process_building_images(
    image_paths=image_paths,
    depth_map_paths=depth_paths,
    output_json_path='all_buildings.json'
)
```

## JSON Output Format

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

## GPT-4 Integration

1. **Run the extraction script** to generate the prompt:
   ```bash
   python extract_building_dimensions.py building.jpg
   ```

2. **Find the prompt file**: `output/building_gpt4_prompt.txt`

3. **Send to GPT-4**:
   - Copy the prompt text
   - Attach the corrected image and depth map
   - Submit to GPT-4 (via API or ChatGPT interface)

4. **Receive refined analysis** in JSON format with:
   - Validated measurements
   - Confidence scores
   - Structural details
   - Analysis notes

## Tips for Best Results

### Image Quality
- Use high-resolution images (minimum 1920x1080)
- Avoid motion blur and poor lighting
- Capture entire building if possible

### Camera Position
- Front-facing views work best
- Minimize viewing angle (< 45° is ideal)
- Include some ground reference

### Reference Points
- Windows, doors, and floors provide scale
- Standard door height ≈ 2.1 meters
- Standard window height ≈ 1.5 meters
- Floor height ≈ 3 meters

## Troubleshooting

### Low Confidence Scores
- Image may be too distant or occluded
- Try processing from different angle
- Provide reference measurements

### Import Errors
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Verify installation
python -c "import torch, cv2, numpy, PIL; print('All imports OK')"
```

### Output Directory Not Created
```bash
# Create manually if needed
mkdir output
```

## Module Reference

| Module | Purpose |
|--------|---------|
| `parallax_correction.py` | Image distortion correction |
| `dimension_extraction.py` | Dimension calculation logic |
| `gpt4_prompts.py` | GPT-4 prompt templates |
| `extract_building_dimensions.py` | Complete pipeline script |
| `examples.py` | Usage examples and demos |

## Documentation

- **README.md** - Main project documentation
- **DIMENSION_EXTRACTION_GUIDE.md** - Detailed usage guide
- **QUICK_REFERENCE.md** - This file (quick reference)

## Support

For issues or questions:
1. Check DIMENSION_EXTRACTION_GUIDE.md for detailed information
2. Review examples.py for code samples
3. Open an issue on GitHub

---

**Happy building measuring! 📏🏢**
