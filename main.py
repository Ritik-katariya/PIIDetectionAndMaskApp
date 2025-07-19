from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
import shutil
import uuid
import os
from utils.ocr import extract_text_with_boxes
from utils.pii_detect import detect_pii
from utils.masker import mask_pii_in_image

app = FastAPI()

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=422, detail="File must be an image")
    
    # Validate file size (max 10MB)
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=422, detail="File size must be less than 10MB")
    
    try:
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
        background_tasks.add_task(os.remove, masked_path)
        background_tasks.add_task(os.remove, file_name)

        return FileResponse(masked_path, media_type="image/jpeg")
    
    except Exception as e:
        # Clean up temp file if it exists
        if 'file_name' in locals() and os.path.exists(file_name):
            os.remove(file_name)
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/")
def hello():
    return {"message": "hello world"}