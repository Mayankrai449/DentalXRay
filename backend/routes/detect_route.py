from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from utils.image_processing import process_and_save_image
from utils.openai_client import generate_diagnostic_report
import os

router = APIRouter()

@router.post("/detect/")
async def detect_objects(file: UploadFile = File(...)):
    try:
        valid_extensions = {".jpg", ".jpeg", ".png", ".dcm", ".rvg"}
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in valid_extensions:
            raise HTTPException(status_code=400, detail="Supported file types: JPEG, PNG, DICOM (.dcm, .rvg)")

        image_bytes = await file.read()

        annotated_image, predictions = process_and_save_image(image_bytes, file_extension, file.filename)

        report = generate_diagnostic_report(predictions)

        response_data = {
            "annotations": predictions,
            "image": annotated_image,
            "diagnostic_report": report
        }

        return JSONResponse(content=response_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")