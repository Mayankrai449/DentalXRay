from PIL import Image, ImageDraw, ImageFont
import io
import base64
import logging
import os
import pydicom
from typing import List, Dict, Tuple
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FONT_SIZE = 30
try:
    FONT = ImageFont.truetype("arial.ttf", FONT_SIZE)
except:
    logger.warning("Arial font not found, using default PIL font")
    FONT = ImageFont.load_default(size=FONT_SIZE)

def convert_dicom_to_jpeg(dicom_bytes: bytes) -> bytes:
    try:
        dicom = pydicom.dcmread(io.BytesIO(dicom_bytes))
        if not hasattr(dicom, 'pixel_array'):
            raise ValueError("DICOM file has no pixel data")
        
        pixel_array = dicom.pixel_array
        pixel_array = ((pixel_array - pixel_array.min()) / (pixel_array.max() - pixel_array.min()) * 255).astype('uint8')
        image = Image.fromarray(pixel_array).convert("RGB")
        output_buffer = io.BytesIO()
        image.save(output_buffer, format="JPEG", quality=95)
        return output_buffer.getvalue()
    except Exception as e:
        logger.error(f"Error converting DICOM to JPEG: {str(e)}")
        if "Unable to decompress" in str(e):
            raise ValueError(
                "DICOM file uses unsupported compression. "
                "Please install 'pylibjpeg' (pip install pylibjpeg pylibjpeg-libjpeg) "
                "or 'gdcm' (pip install python-gdcm) to handle compressed DICOM files."
            )
        raise

def draw_bounding_boxes(image: Image.Image, predictions: List[Dict]) -> Image.Image:
    try:
        draw = ImageDraw.Draw(image)
        
        for pred in predictions:
            x = pred.get("x", 0)
            y = pred.get("y", 0)
            width = pred.get("width", 0)
            height = pred.get("height", 0)
            class_name = pred.get("class", "Unknown")
            confidence = pred.get("confidence", 0.0)
            
            left = x - width / 2
            top = y - height / 2
            right = x + width / 2
            bottom = y + height / 2
            
            draw.rectangle([(left, top), (right, bottom)], outline="red", width=2)
            label = f"{class_name}: {confidence:.2f}"
            label_bbox = draw.textbbox((left, top), label, font=FONT)

            draw.rectangle([(label_bbox[0], label_bbox[1] - FONT_SIZE - 4), (label_bbox[2], label_bbox[3])], fill="red")
            draw.text((left, top - FONT_SIZE - 4), label, fill="white", font=FONT)
        
        return image
    except Exception as e:
        logger.error(f"Error drawing bounding boxes: {str(e)}")
        raise

def process_and_save_image(image_bytes: bytes, file_extension: str, original_filename: str) -> Tuple[str, List[Dict]]:
    try:
        from utils.roboflow_client import call_roboflow_api

        if file_extension in {".dcm", ".rvg"}:
            image_bytes = convert_dicom_to_jpeg(image_bytes)

        predictions = call_roboflow_api(image_bytes)

        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        annotated_image = draw_bounding_boxes(image, predictions)

        os.makedirs("annotated_images", exist_ok=True)

        base_name = re.sub(r'[^\w\-_\. ]', '_', os.path.splitext(original_filename)[0])
        output_path = f"annotated_images/annotated_{base_name}.jpg"
        annotated_image.save(output_path, format="JPEG", quality=95)
        logger.info(f"Annotated image saved to {output_path}")

        output_buffer = io.BytesIO()
        annotated_image.save(output_buffer, format="JPEG", quality=95)
        annotated_image_b64 = base64.b64encode(output_buffer.getvalue()).decode("utf-8")

        return annotated_image_b64, predictions

    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise