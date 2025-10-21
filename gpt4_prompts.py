"""
GPT-4 Prompt Templates for Building Dimension Extraction

This module contains prompt templates for GPT-4 to extract accurate building
dimensions from images with depth maps. The prompts account for parallax
correction and various building structures.
"""

GPT4_DIMENSION_EXTRACTION_PROMPT = """
You are an expert computer vision and architectural measurement AI assistant. Your task is to analyze building images that have been corrected for parallax distortion and are accompanied by depth maps to extract accurate dimensional measurements.

## Input Data:
1. **Corrected Image**: A building photograph that has undergone parallax distortion correction
2. **Depth Map**: A normalized depth map (darker = closer, lighter = farther) corresponding to the image
3. **Image Metadata**: Information about the image capture conditions and any reference measurements

## Your Task:
Analyze the provided image and depth map to extract the following building dimensions:

### Required Measurements:
1. **Width (W)**: The horizontal span of the building facade (in meters)
2. **Height (H)**: The vertical extent from ground to roof/top (in meters)
3. **Depth (D)**: The front-to-back dimension of the building (in meters)
4. **Total Floor Area**: Estimated floor area (in square meters)
5. **Volume**: Approximate building volume (in cubic meters)

### Analysis Steps:
1. **Identify Building Boundaries**:
   - Detect the main building structure in the image
   - Identify corners, edges, and key reference points
   - Account for occluding objects (trees, other buildings, etc.)

2. **Depth Analysis**:
   - Analyze the depth map to understand the 3D structure
   - Identify the building's depth profile
   - Determine distance relationships between different parts

3. **Perspective Considerations**:
   - Account for the viewing angle and camera position
   - Consider how perspective affects apparent dimensions
   - Adjust measurements based on the depth information

4. **Reference Calibration**:
   - If reference measurements are provided, use them for scaling
   - If no references exist, use contextual clues (windows, doors, typical building proportions)
   - Standard door height ≈ 2.1 meters, window height ≈ 1.5 meters, floor height ≈ 3 meters

5. **Uncertainty Assessment**:
   - Evaluate the confidence level of each measurement
   - Identify any ambiguities or occlusions
   - Note any assumptions made

### Output Format:
Provide your analysis in the following JSON format:

```json
{
  "building_id": "building_001",
  "dimensions": {
    "width_meters": <float>,
    "height_meters": <float>,
    "depth_meters": <float>,
    "floor_area_sqm": <float>,
    "volume_cubic_m": <float>
  },
  "confidence_scores": {
    "width": <float 0-1>,
    "height": <float 0-1>,
    "depth": <float 0-1>,
    "overall": <float 0-1>
  },
  "structural_details": {
    "num_floors": <int>,
    "num_visible_windows": <int>,
    "roof_type": "<string>",
    "architectural_style": "<string>"
  },
  "measurement_method": {
    "reference_used": "<string or null>",
    "assumptions": ["<list of key assumptions>"],
    "limitations": ["<list of limitations>"]
  },
  "depth_analysis": {
    "min_depth": <float>,
    "max_depth": <float>,
    "avg_depth": <float>,
    "depth_variance": <float>
  },
  "notes": "<any additional observations or concerns>"
}
```

## Important Considerations:

### Handling Different Building Types:
- **Rectangular Buildings**: Standard width × height × depth calculation
- **L-Shaped Buildings**: Break into segments and sum appropriately
- **Complex Structures**: Provide ranges and note complexity
- **Partially Visible Buildings**: Indicate estimated vs measured portions

### Perspective and Angle Variations:
- **Front-facing view**: Most reliable for width and height
- **Angled view**: Use depth map heavily for depth estimation
- **Elevated view**: Adjust height measurements for viewing angle
- **Ground-level view**: May underestimate height, use depth cues

### Quality Indicators:
- **High Confidence (0.8-1.0)**: Clear boundaries, good depth contrast, reference points available
- **Medium Confidence (0.5-0.8)**: Some occlusion, reasonable depth data, inferred references
- **Low Confidence (0.0-0.5)**: Significant occlusion, poor depth data, no references

### Common Pitfalls to Avoid:
1. Confusing foreground objects with the building
2. Not accounting for camera distortion residuals
3. Ignoring depth map noise or artifacts
4. Over-relying on pixel dimensions without depth scaling
5. Not considering the building's orientation relative to the camera

## Example Scenarios:

### Scenario 1: Modern Office Building (Front View)
- Clear rectangular structure
- Visible floor divisions
- Use window patterns as reference
- Depth map shows uniform facade
→ High confidence measurements possible

### Scenario 2: Historic Building (Angled View)
- Complex architectural details
- Viewing angle ≈ 30-45 degrees
- Depth map shows varying depths
- Use depth gradient for dimension estimation
→ Medium confidence, provide ranges

### Scenario 3: Residential Building (Partially Occluded)
- Trees partially blocking view
- Side view with visible depth
- Estimate hidden portions using visible segments
→ Lower confidence, note assumptions

## Begin Analysis:
Please analyze the provided image and depth map according to the guidelines above and return your findings in the specified JSON format.
"""


GPT4_BATCH_DIMENSION_PROMPT = """
You are analyzing multiple building images with depth maps. For each building:

1. Apply the same rigorous analysis as described in the single-image prompt
2. Ensure consistency in measurement methodology across all buildings
3. If multiple images show the same building from different angles, cross-reference to improve accuracy
4. Provide a summary comparing the buildings

Output Format:
```json
{
  "analysis_summary": {
    "total_buildings": <int>,
    "analysis_timestamp": "<ISO timestamp>",
    "overall_confidence": <float 0-1>
  },
  "buildings": [
    {
      "building_id": "building_001",
      "image_file": "<filename>",
      "dimensions": { ... },
      "confidence_scores": { ... },
      "structural_details": { ... },
      "measurement_method": { ... },
      "depth_analysis": { ... },
      "notes": "<string>"
    },
    // ... more buildings
  ],
  "comparative_analysis": {
    "largest_building": "<building_id>",
    "tallest_building": "<building_id>",
    "average_dimensions": {
      "width": <float>,
      "height": <float>,
      "depth": <float>
    },
    "notes": "<observations about the building collection>"
  }
}
```
"""


GPT4_REFINEMENT_PROMPT = """
You are reviewing previously extracted building dimensions. Your task is to:

1. **Validate** the measurements for physical plausibility
2. **Refine** any measurements that seem inconsistent
3. **Cross-check** dimensions against architectural norms
4. **Identify** and correct any obvious errors

Given:
- Original image and depth map
- Previously extracted dimensions (JSON)
- Any additional context or reference measurements

Provide refined dimensions with explanations for any changes made.

Output the corrected JSON with an additional "refinement_notes" field explaining your adjustments.
"""


def generate_prompt_with_context(
    image_description: str,
    reference_measurements: dict = None,
    building_type: str = "general",
    special_instructions: str = ""
) -> str:
    """
    Generate a customized GPT-4 prompt with specific context.
    
    Args:
        image_description: Description of the image characteristics
        reference_measurements: Dict with any known measurements
        building_type: Type of building (residential, commercial, industrial, etc.)
        special_instructions: Any additional instructions
    
    Returns:
        Customized prompt string
    """
    context = f"\n## Specific Context for This Analysis:\n"
    context += f"- **Image Description**: {image_description}\n"
    context += f"- **Building Type**: {building_type}\n"
    
    if reference_measurements:
        context += "- **Reference Measurements**:\n"
        for key, value in reference_measurements.items():
            context += f"  - {key}: {value}\n"
    
    if special_instructions:
        context += f"- **Special Instructions**: {special_instructions}\n"
    
    return GPT4_DIMENSION_EXTRACTION_PROMPT + context


def format_results_for_gpt4(
    image_path: str,
    depth_map_path: str,
    metadata: dict = None
) -> str:
    """
    Format the input data as a prompt for GPT-4.
    
    Args:
        image_path: Path to the building image
        depth_map_path: Path to the depth map
        metadata: Additional metadata dictionary
    
    Returns:
        Formatted prompt string
    """
    prompt = GPT4_DIMENSION_EXTRACTION_PROMPT + "\n\n"
    prompt += "## Input Files:\n"
    prompt += f"- Image: {image_path}\n"
    prompt += f"- Depth Map: {depth_map_path}\n"
    
    if metadata:
        prompt += "\n## Metadata:\n"
        for key, value in metadata.items():
            prompt += f"- {key}: {value}\n"
    
    prompt += "\n\nPlease proceed with the analysis.\n"
    
    return prompt
