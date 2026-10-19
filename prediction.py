import os
import joblib
import numpy as np
import pandas as pd
from schema.input_data import SmartphoneInputSchema
from schema.response_schema import PredictionResponseSchema, PriceRangeSchema

MODEL_PATH = "models/smartphone_price_model.joblib"
DATA_PATH = "data/processed/cleaned_smartphones.csv"
TEST_MAE = 6564.0  

try:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at path: '{MODEL_PATH}'")
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(
        f"Failed to load machine learning model from '{MODEL_PATH}': {e}"
    )

try:
    df_smartphones = pd.read_csv(DATA_PATH)
except Exception:
    df_smartphones = None


def get_model():
    """Returns the loaded model."""
    if model is None:
        raise RuntimeError("Model is not initialized.")
    return model


def get_similar_phones(min_price: float, max_price: float, limit: int = 4) -> list:
    """Finds sample phones within the predicted price range."""
    if df_smartphones is None or df_smartphones.empty:
        return []

    # Target price column (handles both 'Price' and 'price')
    price_col = "Price" if "Price" in df_smartphones.columns else "price"

    matches = df_smartphones[
        (df_smartphones[price_col] >= min_price) & 
        (df_smartphones[price_col] <= max_price)
    ]

    if matches.empty:
        target_price = (min_price + max_price) / 2
        matches = df_smartphones.iloc[
            (df_smartphones[price_col] - target_price).abs().argsort()[:limit]
        ]
    else:
        matches = matches.sample(min(limit, len(matches)), random_state=42)

    return [
        {
            "phone": str(row["Model"]).title(),
            "price": f"₹{row[price_col]:,.0f}"
        }
        for _, row in matches.iterrows()
    ]


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

        similar_phones_list = get_similar_phones(lower_bound, upper_bound)

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
            similar_phones=similar_phones_list,
        )
    except Exception as e:
        raise RuntimeError(f"Error during smartphone price prediction: {e}")