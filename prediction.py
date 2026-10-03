import joblib
import numpy as np 
import pandas as pd

# Load the trained pipeline once when the module is imported
MODEL_PATH = "D:/Smartphone-Price-Prediction-Project/Smartphone-Price-Prediction-Project/models/smartphone_price_model.joblib"
try:
    pipeline = joblib.load(MODEL_PATH)  
except Exception as e:
    raise RuntimeError(f"Failed to load the model from {MODEL_PATH}: {e}")      


def predict_price(input_data: dict) -> float:
    """
    Predict the price of a smartphone based on input features.

    Parameters:
    input_data (dict): A dictionary containing the features of the smartphone.

    Returns:
    float: The predicted price in Rupees.
    """
    # Convert input data to DataFrame
    input_df = pd.DataFrame([input_data])
    
    # Make prediction using the loaded pipeline
    prediction_log = pipeline.predict(input_df)
    
    # Reverse the log transformation to get actual Rupees
    predicted_price = np.expm1(prediction_log[0])
    
    return predicted_price