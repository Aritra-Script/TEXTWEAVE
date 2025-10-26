"""
ocr_utils Package

Author: Aritra Chakraborty
Author: Shuvomoy Sarkar
Date: 26-Oct-2025
Description:
-------------
This package contains all utilities for OCR processing, including:
- Image preprocessing
- Text extraction using EasyOCR
- Text post-processing
"""

from ocr_utils.reader import extract_text_from_image
from ocr_utils.preprocess import preprocess_image
from ocr_utils.postprocess import clean_text


# Define what is accessible when importing ocr_utils directly
__all__ = ["extract_text_from_image", "preprocess_image", "clean_text"]
