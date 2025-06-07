import requests
import base64
import logging
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")
ROBOFLOW_MODEL_ENDPOINT = "https://detect.roboflow.com/adr/6"
CONFIDENCE_THRESHOLD = 0.3
OVERLAP_THRESHOLD = 0.5

def call_roboflow_api(image_bytes: bytes) -> List[Dict]:
    try:
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        headers = {
            "Authorization": f"Bearer {ROBOFLOW_API_KEY}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        params = {
            "api_key": ROBOFLOW_API_KEY,
            "confidence": CONFIDENCE_THRESHOLD,
            "overlap": OVERLAP_THRESHOLD
        }

        logger.info("Sending request to Roboflow API")
        response = requests.post(
            ROBOFLOW_MODEL_ENDPOINT,
            data=image_b64,
            headers=headers,
            params=params
        )

        if response.status_code != 200:
            logger.error(f"Roboflow API error: {response.status_code} - {response.text}")
            raise Exception(f"Roboflow API error: {response.status_code}")

        predictions = response.json().get("predictions", [])
        logger.info(f"Received {len(predictions)} predictions from Roboflow")
        return predictions

    except Exception as e:
        logger.error(f"Error calling Roboflow API: {str(e)}")
        raise