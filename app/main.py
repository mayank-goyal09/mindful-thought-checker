import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import uvicorn

from app.predictor import CognitiveDistortionPredictor
from app.distortions_db import DISTORTIONS_MAP

app = FastAPI(
    title="Cognitive Distortion Detector API",
    description="A production-grade REST API serving a DistilBERT model optimized via ONNX Runtime to detect cognitive distortions in text.",
    version="1.0.0"
)

# Enable CORS for external products
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Input Pydantic Model
class PredictionRequest(BaseModel):
    text: str = Field(
        ..., 
        example="I got a B on the exam. I should always get A's, I'm completely useless.",
        min_length=1, 
        description="The statement or thought to analyze for cognitive distortions."
    )

# Individual Distortion Output Model
class DistortionDetails(BaseModel):
    name: str
    description: str
    examples: List[str]
    reframing_questions: List[str]
    reframing_advice: str

# API Response Model
class PredictionResponse(BaseModel):
    text: str
    predicted_distortion: str
    confidence: float
    latency_ms: float
    distortion_details: DistortionDetails
    all_probabilities: Dict[str, float]

# Global predictor instance
predictor = None

@app.on_event("startup")
def startup_event():
    global predictor
    model_dir = os.environ.get("MODEL_DIR", "./MentalHealth_AI_Model")
    try:
        predictor = CognitiveDistortionPredictor.get_instance(model_dir)
        print("Production model loaded and initialized successfully!")
    except Exception as e:
        print(f"Error loading model on startup: {str(e)}")
        # We don't crash the server immediately, but routes will return 503

@app.get("/health")
def health_check():
    if predictor is None:
        return {"status": "unhealthy", "error": "Model not loaded yet"}
    return {
        "status": "healthy",
        "model_engine": "ONNX Runtime",
        "model_file": predictor.onnx_path,
        "classes_loaded": len(DISTORTIONS_MAP)
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    if predictor is None:
        raise HTTPException(
            status_code=503, 
            detail="Service Unavailable: Model not loaded."
        )
    
    try:
        # Run prediction
        res = predictor.predict(request.text)
        
        label_id = res["label_id"]
        confidence = res["confidence"]
        latency_ms = res["latency_ms"]
        probs = res["probabilities"]
        
        # Look up metadata from db
        details = DISTORTIONS_MAP.get(label_id)
        if details is None:
            raise HTTPException(
                status_code=500,
                detail=f"Label ID {label_id} not found in distortions map."
            )
            
        # Format the probabilities mapping for response (using string names instead of digits)
        all_probs_named = {
            DISTORTIONS_MAP[idx]["name"]: prob for idx, prob in probs.items()
        }
        
        return PredictionResponse(
            text=request.text,
            predicted_distortion=details["name"],
            confidence=confidence,
            latency_ms=latency_ms,
            distortion_details=DistortionDetails(**details),
            all_probabilities=all_probs_named
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error executing prediction: {str(e)}"
        )

if __name__ == "__main__":
    # Start the server locally
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
