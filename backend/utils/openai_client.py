import openai
import logging
import json
from typing import List, Dict
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_diagnostic_report(predictions: List[Dict]) -> Dict:
    try:
        prompt = f"""
You are an expert dental radiologist. Based on the provided image annotations from an object detection model, generate a diagnostic report in professional clinical language. The annotations include detected pathologies, their locations (bounding box coordinates), and confidence scores. Output a JSON object with the following structure:
- "Diagnosis": A brief paragraph summarizing detected pathologies and their locations (e.g., upper left molar, if inferable from coordinates) with some insights and diagnosis information.
- "Details": A list of objects, each containing pathology name, location (e.g., upper left molar), coordinates (x, y, width, height), and confidence score.
- "ClinicalAdvice": A list of actionable recommendations for the patient or dentist.
Ensure the report is clear, concise, and suitable for clinical use.
Annotations: {json.dumps(predictions)}
"""

        client = openai.OpenAI()
        response = client.responses.create(
            model="gpt-4.1-nano",
            input=prompt
        )

        report = json.loads(response.output_text)
        logger.info("Diagnostic report generated successfully")
        return report

    except Exception as e:
        logger.error(f"Error generating diagnostic report: {str(e)}")
        raise