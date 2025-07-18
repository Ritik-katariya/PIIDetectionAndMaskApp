import cv2
import easyocr
reader = easyocr.Reader(['en'])

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    return thresh

def extract_text_with_boxes(image_path):
    image = preprocess_image(image_path)
    results = reader.readtext(image)
    return results
