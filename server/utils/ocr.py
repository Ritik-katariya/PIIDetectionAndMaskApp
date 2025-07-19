import cv2
import easyocr
import os

reader = easyocr.Reader(['en'], gpu=False, verbose=False, download_enabled=False)

def preprocess_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Unable to read image from path: {image_path}")
    
    height, width = img.shape[:2]
    if max(height, width) > 1200:
        img = cv2.resize(img, (width // 2, height // 2))
    return img

def extract_text_with_boxes(image_path):
    try:
        image = preprocess_image(image_path)
        results = reader.readtext(image)
        return results
    except Exception as e:
        raise Exception(f"OCR processing failed: {str(e)}")
