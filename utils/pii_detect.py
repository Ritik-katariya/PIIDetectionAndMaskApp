import re

# Enhanced regex patterns for Aadhaar and other PII
PII_REGEX = {
    "aadhaar": r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b",
    "phone": r"\b(?:\+91[\s\-]?)?[6-9]\d{9}\b",
    "dob": r"\b(?:DOB\s*[:\-]?\s*)?(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{4})\b",
    "email": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
    # Name: lines with 'Name' or likely full names (2+ capitalized words, not all uppercase)
    "name": r"(?i)\bname\b\s*[:\-]?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)|\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b",
    # Address: lines with 'Address' or likely address patterns
    "address": r"(?i)\baddress\b\s*[:\-]?\s*([A-Za-z0-9\s,\-\.]+)|\b([A-Za-z0-9\s,\-]{10,})\b",
}

def detect_pii(ocr_results):
    """
    Detect PII in OCR text lines for Aadhaar cards.
    Returns a list of dicts: [{bbox, label, text, confidence}]
    """
    pii_boxes = []
    for bbox, text, conf in ocr_results:
        for label, pattern in PII_REGEX.items():
            # For name/address, try to avoid false positives by context
            if label in ["name", "address"]:
                matches = re.findall(pattern, text)
                for match in matches:
                    # match can be a tuple if multiple groups
                    value = next((m for m in match if m), None)
                    if value and len(value) > 2:
                        pii_boxes.append({
                            "bbox": bbox,
                            "label": label,
                            "text": value.strip(),
                            "confidence": conf
                        })
                        break
            else:
                match = re.search(pattern, text)
                if match:
                    pii_boxes.append({
                        "bbox": bbox,
                        "label": label,
                        "text": match.group(0),
                        "confidence": conf
                    })
                    break
    return pii_boxes
