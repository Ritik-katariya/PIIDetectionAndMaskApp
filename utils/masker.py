import cv2

def mask_pii_in_image(image_path, pii_boxes):
    img = cv2.imread(image_path)

    for box in pii_boxes:
        # box = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        x_coords = [point[0] for point in box]
        y_coords = [point[1] for point in box]
        x1, y1 = min(x_coords), min(y_coords)
        x2, y2 = max(x_coords), max(y_coords)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), -1)  # Fill black

    masked_path = f"{image_path}_masked.jpg"
    cv2.imwrite(masked_path, img)
    return masked_path
