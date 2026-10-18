import os
import joblib
import numpy as np
import pandas as pd
from schema.input_data import SmartphoneInputSchema
from schema.response_schema import PredictionResponseSchema, PriceRangeSchema

MODEL_PATH = "models/smartphone_price_model.joblib"
TEST_MAE = 6564.0  

try:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at path: '{MODEL_PATH}'")
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(
        f"Failed to load machine learning model from '{MODEL_PATH}': {e}"
    )


def get_model():
    """Returns the loaded model."""
    if model is None:
        raise RuntimeError("Model is not initialized.")
    return model


def categorize_segment(price: float) -> str:
    """Categorizes smartphone based on price."""
    if price < 15000:
        return "Budget"
    elif price < 30000:
        return "Mid-Range"
    elif price < 60000:
        return "Premium"
    return "Flagship Tier"


def run_prediction(input_data: SmartphoneInputSchema) -> PredictionResponseSchema:
    """Runs model inference and formats the rich output response."""
    try:
    
        data_dict = input_data.model_dump(by_alias=True)
        input_df = pd.DataFrame([data_dict])

    
        log_price = model.predict(input_df)[0]
        predicted_price = float(np.expm1(log_price))
        predicted_price = round(max(1000.0, predicted_price), 2)

        lower_bound = round(max(1000.0, predicted_price - TEST_MAE), 2)
        upper_bound = round(predicted_price + TEST_MAE, 2)

        return PredictionResponseSchema(
            predicted_price_inr=predicted_price,
            formatted_price=f"₹{predicted_price:,.2f}",
            market_segment=categorize_segment(predicted_price),
            price_range=PriceRangeSchema(
                lower_bound_inr=lower_bound, upper_bound_inr=upper_bound
            ),
            confidence_score=0.90,
            dominant_features={
                "Brand": str(data_dict.get("Brand")),
                "Processor": str(data_dict.get("ProcessorName")),
                "Memory": (
                    f"{int(data_dict.get('Ram', 0))}GB RAM / "
                    f"{int(data_dict.get('Rom', 0))}GB ROM"
                ),
            },
        )
    except Exception as e:
        raise RuntimeError(f"Error during smartphone price prediction: {e}")