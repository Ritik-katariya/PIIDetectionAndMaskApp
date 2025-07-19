import cv2
import os

def mask_pii_in_image(image_path, pii_boxes):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Unable to read image from path: {image_path}")

    # Validate pii_boxes
    if not isinstance(pii_boxes, list):
        raise ValueError("pii_boxes must be a list")

    for box in pii_boxes:
        if not isinstance(box, list) or len(box) != 4:
            continue  # Skip invalid boxes
            
        try:
            # box = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
            x_coords = [point[0] for point in box if len(point) >= 2]
            y_coords = [point[1] for point in box if len(point) >= 2]
            
            if not x_coords or not y_coords:
                continue
                
            x1, y1 = min(x_coords), min(y_coords)
            x2, y2 = max(x_coords), max(y_coords)

            # Ensure coordinates are within image bounds
            height, width = img.shape[:2]
            x1 = max(0, min(x1, width - 1))
            y1 = max(0, min(y1, height - 1))
            x2 = max(0, min(x2, width - 1))
            y2 = max(0, min(y2, height - 1))

            # Option 1: Fill with black
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), -1)

            # Option 2: Blur instead (uncomment below)
            # roi = img[y1:y2, x1:x2]
            # img[y1:y2, x1:x2] = cv2.GaussianBlur(roi, (31, 31), 0)
        except Exception as e:
            # Skip this box if there's an error
            continue

    base, ext = os.path.splitext(image_path)
    masked_path = f"{base}_masked{ext}"
    
    success = cv2.imwrite(masked_path, img)
    if not success:
        raise ValueError(f"Failed to save masked image to: {masked_path}")
    
    return masked_path
