# Dental AI Pathology

A web application for automated dental pathology detection using AI. Upload dental images and receive instant diagnostic reports with annotated results.

## Overview

Dental AI Pathology combines computer vision and natural language processing to analyze dental X-rays and images. The system detects pathologies like cavities using Roboflow's object detection API and generates detailed diagnostic reports using OpenAI's language models.

**Key Components:**
- **Frontend**: React.js web interface for image upload and results display
- **Backend**: FastAPI server handling image processing and AI analysis
- **AI Integration**: Roboflow for pathology detection + OpenAI for report generation

## Features

- **Multi-format Support**: Upload dental images in .dcm, .rvg, or standard formats (JPEG, PNG)
- **AI-Powered Detection**: Automated identification of dental pathologies like cavities
- **Visual Annotations**: View detected pathologies highlighted on your images
- **Diagnostic Reports**: Detailed clinical reports with recommendations

![Main](/images/main.png)

## Setup Instructions

### Prerequisites

**Install Python 3.12.6:**
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **Mac**: Use Homebrew: `brew install python@3.12`
- **Linux**: `sudo apt update && sudo apt install python3.12 python3.12-venv`

**Install Node.js 18.20.4:**
- **All platforms**: Download from [nodejs.org](https://nodejs.org/)
- **Mac**: Use Homebrew: `brew install node@18`
- **Linux**: Use NodeSource: `curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs`

**Get API Keys:**
- **OpenAI API Key**: Sign up at [platform.openai.com](https://platform.openai.com/) → API Keys
- **Roboflow API Key**: Sign up at [roboflow.com](https://roboflow.com/) → Account Settings → API

### Manual Setup

**Step 1: Setup Backend**
```bash
# Clone and navigate to backend
git clone https://github.com/Mayankrai449/DentalXRay.git
cd DentalXRay/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
echo "OPENAI_API_KEY=your-openai-api-key" > .env
echo "ROBOFLOW_API_KEY=your-roboflow-api-key" >> .env

# Start backend server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Step 2: Setup Frontend (New Terminal)**
```bash
# Navigate to frontend directory
cd DentalXRay/frontend

# Install dependencies
npm install

# Start development server
npm start
```

The application will open automatically at `http://localhost:3000`.

### Optional: Docker Setup

For easier deployment, you can use Docker instead of manual setup:

**Step 1: Install Docker**
- **Windows/Mac**: Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/)
- **Linux**: Run `curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh`

**Step 2: Run with Docker**
```bash
# Clone the repository
git clone https://github.com/Mayankrai449/DentalXRay.git
cd DentalXRay

# Create environment file
echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
echo "ROBOFLOW_API_KEY=your-roboflow-api-key-here" >> .env

# Start the application
docker-compose up --build
```

Access the application at `http://localhost:3000` and API documentation at `http://localhost:8000/docs`.

## Usage Guide

### Uploading Images
1. Open the application in your browser (`http://localhost:3000`)
2. Click the central "Upload" button
3. Select a dental image file (.dcm, .rvg, .jpg, .png)
4. Wait for the AI analysis to complete

### Understanding Results
- **Left Panel**: Annotated image showing detected pathologies
- **Right Panel**: Detailed diagnostic report with clinical recommendations

### Sample Analysis Output
The system provides structured results including:
- **Pathology Detection**: Location and confidence scores for detected issues
- **Visual Annotations**: Bounding boxes highlighting problem areas
- **Clinical Report**: Professional diagnostic summary with treatment recommendations

## API Reference

### Endpoints

**POST `/detect/`**
- **Purpose**: Analyze dental image for pathologies
- **Input**: Multipart form-data with `file` key containing image
- **Output**: JSON response with annotations, annotated image, and diagnostic report

**Example Response:**
```json
{
    "annotations": [
        {
            "x": 409.0,
            "y": 531.5,
            "width": 210.0,
            "height": 245.0,
            "confidence": 0.802386462688446,
            "class": "cavity",
            "class_id": 0,
            "detection_id": "2e7e75bc-dabf-4b72-8e80-550be2cdfd69"
        }
    ],
    "image": "/9j/4AAQSkZJRgABAQAAAQ..9k=",
    "diagnostic_report": {
        "Diagnosis": "The detection indicates the presence of a dental cavity...",
        "Details": [
            {
                "pathology": "cavity",
                "location": "posterior molar region",
                "coordinates": {
                    "x": 409.0,
                    "y": 531.5,
                    "width": 210.0,
                    "height": 245.0
                },
                "confidence": 0.8024
            }
        ],
        "ClinicalAdvice": [
            "Schedule a comprehensive clinical examination",
            "Consider restorative treatment options",
            "Evaluate for possible pulp vitality testing",
            "Implement preventive measures"
        ]
    }
}
```