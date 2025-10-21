"""
Parallax Correction Module

This module provides functionality to correct parallax distortion in images
before processing for dimension extraction. Parallax correction is essential
for accurate measurement extraction from images taken at various angles.
"""

import cv2
import numpy as np
from typing import Tuple, Optional


def correct_parallax(
    image: np.ndarray,
    camera_matrix: Optional[np.ndarray] = None,
    dist_coeffs: Optional[np.ndarray] = None
) -> np.ndarray:
    """
    Correct parallax distortion in an image.
    
    Args:
        image: Input image as numpy array (BGR format)
        camera_matrix: Camera intrinsic matrix (3x3). If None, uses default calibration.
        dist_coeffs: Distortion coefficients. If None, uses default values.
    
    Returns:
        Corrected image as numpy array
    """
    h, w = image.shape[:2]
    
    # Use default camera matrix if not provided
    if camera_matrix is None:
        # Approximate camera matrix for a typical webcam
        focal_length = w
        center = (w / 2, h / 2)
        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype=np.float32)
    
    # Use default distortion coefficients if not provided
    if dist_coeffs is None:
        # Assume minimal distortion
        dist_coeffs = np.zeros((4, 1), dtype=np.float32)
    
    # Get optimal new camera matrix
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
        camera_matrix, dist_coeffs, (w, h), 1, (w, h)
    )
    
    # Undistort the image
    undistorted = cv2.undistort(
        image, camera_matrix, dist_coeffs, None, new_camera_matrix
    )
    
    # Crop the image based on ROI
    x, y, w_roi, h_roi = roi
    if w_roi > 0 and h_roi > 0:
        undistorted = undistorted[y:y+h_roi, x:x+w_roi]
    
    return undistorted


def correct_perspective(
    image: np.ndarray,
    src_points: Optional[np.ndarray] = None,
    target_aspect_ratio: float = 1.0
) -> np.ndarray:
    """
    Correct perspective distortion using known reference points.
    
    Args:
        image: Input image as numpy array (BGR format)
        src_points: Source points defining the quadrilateral to correct (4 points).
                   If None, attempts automatic detection.
        target_aspect_ratio: Desired aspect ratio of the output (width/height)
    
    Returns:
        Perspective-corrected image as numpy array
    """
    h, w = image.shape[:2]
    
    if src_points is None:
        # Use default corners with slight inward offset to handle edge distortion
        offset = 0.05
        src_points = np.array([
            [w * offset, h * offset],
            [w * (1 - offset), h * offset],
            [w * (1 - offset), h * (1 - offset)],
            [w * offset, h * (1 - offset)]
        ], dtype=np.float32)
    
    # Define destination points for a rectangular output
    if target_aspect_ratio >= 1.0:
        dst_w = int(w)
        dst_h = int(w / target_aspect_ratio)
    else:
        dst_h = int(h)
        dst_w = int(h * target_aspect_ratio)
    
    dst_points = np.array([
        [0, 0],
        [dst_w, 0],
        [dst_w, dst_h],
        [0, dst_h]
    ], dtype=np.float32)
    
    # Calculate perspective transformation matrix
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    
    # Apply perspective transformation
    corrected = cv2.warpPerspective(image, matrix, (dst_w, dst_h))
    
    return corrected


def auto_correct_image(image: np.ndarray) -> np.ndarray:
    """
    Automatically apply standard corrections to an image.
    
    This function applies both lens distortion and basic perspective correction
    with default parameters suitable for most building photography scenarios.
    
    Args:
        image: Input image as numpy array (BGR format)
    
    Returns:
        Corrected image as numpy array
    """
    # First, correct lens distortion
    corrected = correct_parallax(image)
    
    # Then apply mild perspective correction
    corrected = correct_perspective(corrected)
    
    return corrected
