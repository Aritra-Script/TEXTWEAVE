"""
Preprocessing Utilities for OCR

Author: Aritra Chakraborty
Author: Shuvomoy Sarkar
Date: 26-Oct-2025
Description:
-------------
Contains functions to preprocess images before feeding them to OCR.
Preprocessing improves OCR accuracy by enhancing image quality.
"""

import cv2
import numpy as np

def preprocess_image(image_path: str) -> np.ndarray:
    """
    Load and preprocess an image for OCR.

    Steps:
    1. Read image in grayscale
    2. Apply thresholding / adaptive thresholding
    3. Optional: noise reduction (Gaussian blur)
    4. Return preprocessed image

    Parameters:
    -----------
    image_path : str
        Path to the input image file

    Returns:
    --------
    np.ndarray
        Preprocessed image ready for OCR
    """
    # Read image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Apply Gaussian blur to reduce noise
    img_blur = cv2.GaussianBlur(img, (5, 5), 0)

    # Apply adaptive thresholding to enhance contrast
    img_thresh = cv2.adaptiveThreshold(
        img_blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return img_thresh
