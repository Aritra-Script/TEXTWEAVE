"""
Post-processing Utilities for OCR

Author: Aritra Chakraborty
Author: Shuvomoy Sarkar
Date: 26-Oct-2025
Description:
-------------
Contains functions to clean and normalize text extracted from OCR.
Removes unwanted characters, corrects spacing, and fixes minor OCR errors.
"""

import re

def clean_text(text: str) -> str:
    """
    Clean OCR extracted text.

    Steps:
    1. Remove extra spaces and newlines
    2. Remove non-printable characters
    3. Optional: fix common OCR mistakes (e.g., '0' -> 'O', '1' -> 'I')

    Parameters:
    -----------
    text : str
        Raw text extracted from OCR

    Returns:
    --------
    str
        Cleaned and readable text
    """
    # Remove non-printable characters
    text = re.sub(r'[^\x20-\x7E]', '', text)

    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text
