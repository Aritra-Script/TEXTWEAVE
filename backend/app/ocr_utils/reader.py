"""
OCR Reader using EasyOCR

Author: Aritra Chakraborty
Author: Shuvomoy Sarkar
Date: 26-Oct-2025
Description:
-------------
Contains function to extract text from an image using EasyOCR.
Supports handwriting and printed text recognition.
"""

import easyocr
from ocr_utils.preprocess import preprocess_image
from ocr_utils.postprocess import clean_text

# Initialize EasyOCR reader globally to avoid reloading every request
# English language; you can add more languages like ['en','hi'] if needed
reader = easyocr.Reader(['en'], gpu=True)  # Set gpu=True if you have CUDA

def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from an image file using EasyOCR.

    Steps:
    1. Preprocess the image to enhance OCR accuracy
    2. Use EasyOCR to read text
    3. Post-process the text to clean it

    Parameters:
    -----------
    image_path : str
        Path to the input image file

    Returns:
    --------
    str
        Cleaned extracted text from the image
    """
    # Preprocess the image
    preprocessed_img = preprocess_image(image_path)

    # Perform OCR
    result = reader.readtext(preprocessed_img)

    # Concatenate detected text
    raw_text = " ".join([text[1] for text in result])

    # Post-process text (cleanup)
    cleaned_text = clean_text(raw_text)

    return cleaned_text
