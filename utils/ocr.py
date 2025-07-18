import easyocr

reader = easyocr.Reader(['en'])

def extract_text_with_boxes(image_path):
    results = reader.readtext(image_path)
    return results  # List of (bbox, text, confidence)
