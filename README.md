# Aadhaar PII Masker

A Python FastAPI application to detect and mask Personally Identifiable Information (PII) from Indian Aadhaar card images using OCR and computer vision.

## Features
- Detects and masks the following PII:
  - Full Name
  - Address
  - Date of Birth
  - Aadhaar Number
  - Phone Number
  - Email Address
- Uses EasyOCR for text extraction
- Masks detected PII regions in the image
- Auto-deletes temporary files after processing

## Setup
1. **Clone the repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

## Usage
- Send a POST request to `/upload/` with an Aadhaar image file (JPEG).
- The API returns the masked image with PII hidden.

Example using `curl`:
```bash
curl -F "file=@your_aadhaar.jpg" http://localhost:8000/upload/ --output masked.jpg
```

## Project Structure
- `main.py` - FastAPI app and endpoints
- `utils/ocr.py` - OCR and preprocessing
- `utils/pii_detect.py` - PII detection logic
- `utils/masker.py` - Image masking

## Contact
For questions or issues, please open an issue or contact the maintainer. 