from typing import Dict
from pydantic import BaseModel, Field


class PriceRangeSchema(BaseModel):
  lower_bound_inr: float = Field(
      ..., description="Estimated lower bound based on test MAE"
  )
  upper_bound_inr: float = Field(
      ..., description="Estimated upper bound based on test MAE"
  )


class PredictionResponseSchema(BaseModel):
  predicted_price_inr: float
  formatted_price: str
  market_segment: str
  price_range: PriceRangeSchema
  confidence_score: float = Field(
      ...,
      description=(
          "Confidence metric (0.0 to 1.0) derived from model R2 and hardware"
          " sanity"
      ),
  )
  dominant_features: Dict[str, str] = Field(
      ..., description="Key specs driving this prediction"
  )


class HealthResponseSchema(BaseModel):
  status: str
  model_loaded: bool
  service: str


class ModelMetadataResponseSchema(BaseModel):
  model_name: str
  algorithm: str
  r2_score: float
  mae_inr: float
  target_transformation: str
  feature_count: int