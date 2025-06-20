from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.detect_route import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Dental Pathology Detection")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)