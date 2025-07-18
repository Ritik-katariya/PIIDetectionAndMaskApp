from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
import shutil
import uuid
import os
from utils.ocr import extract_text_with_boxes
from utils.pii_detect import detect_pii
from utils.masker import mask_pii_in_image

app = FastAPI()

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    # Save temp file
    file_name = f"temp_{uuid.uuid4()}.jpg"
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # OCR to get text and positions
    results = extract_text_with_boxes(file_name)

    # Detect PII
    pii_results = detect_pii(results)
    pii_boxes = [item["bbox"] for item in pii_results]

    # Mask PII
    masked_path = mask_pii_in_image(file_name, pii_boxes)

    # Schedule file deletion after response
    if background_tasks is not None:
        background_tasks.add_task(os.remove, masked_path)
        background_tasks.add_task(os.remove, file_name)

    return FileResponse(masked_path, media_type="image/jpeg")

@app.get("/")
def hello():
    return {"message": "hello world"}