import re

# Define regex for Aadhaar, email, phone etc.
PII_REGEX = {
    # Matches XXXX XXXX XXXX format
    "aadhaar": r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b",

    # Matches standard Indian mobile numbers starting with 6-9
    "phone": r"\b[6-9]\d{9}\b",

    # Matches common DOB formats: DD/MM/YYYY or DD-MM-YYYY
    "dob": r"\b(?:DOB\s*[:\-]?\s*)?(\d{2}[/\-]\d{2}[/\-]\d{4})\b",

    # Matches email addresses
    "email": r"\b[\w\.-]+@[\w\.-]+\.\w+\b",

    # Matches lines starting with Name: or NAME or Name of the holder etc.
    "name": r"(?i)\b(name\s*(of\s*(the\s*)?(holder)?)?\s*[:\-]?\s*)([A-Z][A-Z\s]+)",

    # Matches Address: or anything starting with address (case-insensitive)
    "address": r"(?i)\b(address\s*[:\-]?\s*)(.+)",
}

def detect_pii(ocr_results):
    pii_boxes = []
    for bbox, text, conf in ocr_results:
        for label, pattern in PII_REGEX.items():
            if re.search(pattern, text):
                pii_boxes.append(bbox)
                break
    return pii_boxes
    