from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schema.input_data import BatchSmartphoneInputSchema, SmartphoneInputSchema
from prediction import run_prediction
from schema.response_schema import (HealthResponseSchema, ModelMetadataResponseSchema, PredictionResponseSchema,)

app = FastAPI(
    title="Smartphone Price Prediction API",
    description="Simple REST API to estimate smartphone market prices",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home() -> Dict[str, str]:
  return {
      "message": "Welcome to Smartphone Price Prediction API",
      "docs": "/docs",
      "health": "/health",
  }


@app.get("/health", response_model=HealthResponseSchema)
def health():
  return HealthResponseSchema(
      status="healthy",
      model_loaded=True,
      service="Smartphone Price Prediction API",
  )


@app.get("/model/metadata", response_model=ModelMetadataResponseSchema)
def model_info():
  return ModelMetadataResponseSchema(
      model_name="XGBoost Smartphone Price Predictor",
      algorithm="XGBoost Regressor (Pipeline)",
      r2_score=0.8985,
      mae_inr=6564.0,
      target_transformation="np.log1p",
      feature_count=27,
  )


@app.post("/predict", response_model=PredictionResponseSchema)
def predict(payload: SmartphoneInputSchema):
  try:
    return run_prediction(payload)
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/batch", response_model=List[PredictionResponseSchema])
def predict_batch(payload: BatchSmartphoneInputSchema): 
  try:
    return [run_prediction(device) for device in payload.devices]
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))