# MiDaS Webcam Depth Estimation

This project demonstrates **real-time monocular depth estimation** using the MiDaS model and a regular webcam feed. No depth sensor is required.

![Demo GIF](demo_midas-webcam-depth-estimation.gif)

## Motivation
Depth estimation is a crucial building block for AR/VR, robotics, and computer vision. By leveraging state-of-the-art pretrained models like MiDaS, we can approximate scene depth in real-time using just a regular webcam. This project was created to:

- Experiment with MiDaS in a live setting
- Test integration with live webcam inputs
- Prepare for further fusion with object detection (YOLO) and distance conversion tools

## Model
This project uses the [MiDaS v3.1 Small](https://github.com/isl-org/MiDaS) model from the `torch.hub` repository.

## Features

### Real-time Depth Estimation
- Live webcam feed depth estimation
- No depth sensor required
- Visualized depth maps with color coding

### Building Dimension Extraction
- **Parallax Correction**: Automatically corrects lens and perspective distortion
- **Depth Map Generation**: Uses MiDaS for accurate depth estimation
- **Dimension Calculation**: Extracts width, height, depth, area, and volume
- **JSON Output**: Structured output format for easy integration
- **GPT-4 Integration**: Provides detailed prompts for AI-assisted analysis
- **Batch Processing**: Process multiple buildings at once
- **Confidence Scoring**: Evaluates measurement reliability

## Tech Stack
- Python 3.10+
- PyTorch
- OpenCV
- timm (for model loading)
- Conda environment (not virtualenv)

## Folder Structure
```
├── cam_check.py                    # Simple webcam test script
├── realtime_midas_depth.py        # Main depth estimation logic
├── parallax_correction.py         # Parallax distortion correction module
├── dimension_extraction.py        # Building dimension extraction module
├── gpt4_prompts.py                # GPT-4 prompt templates
├── extract_building_dimensions.py # Complete dimension extraction workflow
├── demo_midas-webcam-depth-estimation.gif  # Demo output for README
├── LICENSE
├── .gitignore
├── README.md                      # This file
├── requirements.txt
```

## How to Run
### 1. Clone the Repository
```bash
git clone https://github.com/JANGRAEJO/midas-webcam-depth-estimation.git
cd midas-webcam-depth-estimation
```

### 2. Create and Activate Conda Environment
```bash
conda create -n midas-depth python=3.10 -y
conda activate midas-depth
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Webcam Depth Estimation
```bash
python realtime_midas_depth.py
```

### 5. Extract Building Dimensions from Images
For extracting dimensions from building images with depth maps:

```bash
# Process a single image
python extract_building_dimensions.py path/to/building.jpg

# Process multiple images
python extract_building_dimensions.py image1.jpg image2.jpg image3.jpg

# View GPT-4 prompt template
python extract_building_dimensions.py --show-prompt
```

The script will:
1. Apply parallax correction to the input image
2. Generate a depth map using MiDaS
3. Extract building dimensions (width, height, depth, area, volume)
4. Save results in JSON format
5. Generate a GPT-4 prompt for further analysis

Output files will be saved in the `output/` directory by default.

## File Descriptions
### `cam_check.py`
Runs a quick test to make sure the webcam is functioning correctly using OpenCV.

### `realtime_midas_depth.py`
Main script that loads MiDaS, grabs webcam frames, preprocesses them, and shows the depth estimation output in real-time.

### `extract_building_dimensions.py`
Complete pipeline for extracting building dimensions from images. This script:
- Corrects parallax distortion in building images
- Generates depth maps using MiDaS
- Extracts dimensional measurements (width, height, depth, area, volume)
- Generates GPT-4 prompts for further analysis
- Outputs results in JSON format

**Usage:**
```bash
# Process a single building image
python extract_building_dimensions.py building.jpg

# Process multiple images
python extract_building_dimensions.py building1.jpg building2.jpg building3.jpg

# Skip parallax correction
python extract_building_dimensions.py building.jpg --no-parallax-correction

# Specify output directory
python extract_building_dimensions.py building.jpg --output-dir results

# View the GPT-4 prompt template
python extract_building_dimensions.py --show-prompt
```

### `parallax_correction.py`
Module for correcting parallax distortion in images before dimension extraction. Includes:
- Lens distortion correction
- Perspective correction
- Automatic correction with default parameters

### `dimension_extraction.py`
Module for extracting building dimensions from images with depth maps. Features:
- Edge detection and contour analysis
- Dimension calculation from depth information
- JSON output format
- Batch processing capabilities

### `gpt4_prompts.py`
GPT-4 prompt templates for analyzing building images with depth maps. The prompts:
- Guide GPT-4 to extract accurate dimensions
- Account for various building structures and perspectives
- Provide detailed instructions for handling edge cases
- Support both single and batch processing

## Requirements
Check `requirements.txt` for all required packages.

```txt
torch>=2.0.0
torchvision
opencv-python
timm
Pillow
```

## Limitations
- Output is relative depth, not absolute distances.
- FPS may vary depending on hardware (MiDaS is heavy on CPU/GPU).

## Next Steps
- Integrate with YOLOv9 for object detection + distance annotation
- Calibrate real-world scaling using known markers or camera parameters
- Build web app or GUI using Streamlit or Flask
- Enhance dimension extraction with machine learning-based segmentation
- Support for 3D model reconstruction from multiple views

## Author
**Jangrae Jo**  
MS in ECE, UMass Amherst  
Open to research and collaboration in computer vision and depth sensing.

## License
MIT License – see [LICENSE](LICENSE) file.

---
> If this project helps you, please ⭐ the repo and follow for more updates!
