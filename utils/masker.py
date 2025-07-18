import cv2
import os

def mask_pii_in_image(image_path, pii_boxes):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Unable to read image from path: {image_path}")

    for box in pii_boxes:
        # box = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        x_coords = [point[0] for point in box]
        y_coords = [point[1] for point in box]
        x1, y1 = min(x_coords), min(y_coords)
        x2, y2 = max(x_coords), max(y_coords)

        # Option 1: Fill with black
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), -1)

        # Option 2: Blur instead (uncomment below)
        # roi = img[y1:y2, x1:x2]
        # img[y1:y2, x1:x2] = cv2.GaussianBlur(roi, (31, 31), 0)

    base, ext = os.path.splitext(image_path)
    masked_path = f"{base}_masked{ext}"
    cv2.imwrite(masked_path, img)
    return masked_path
