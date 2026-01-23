# Utility functions for extracting text from PDF files

import PyPDF2
from typing import Tuple, Optional, IO


def extract_text_from_pdf(file: IO[bytes]) -> Tuple[str, Optional[str]]:
    """
    Extract text from an uploaded PDF file.

    Args:
        file: A file-like object (Streamlit uploaded file supports this).

    Returns:
        A tuple (text, error_message). If extraction succeeds, error_message is None.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text, None
    except Exception as e:
        # Return an empty string and the stringified exception for the caller to handle
        return "", f"Failed to read PDF: {e}"
