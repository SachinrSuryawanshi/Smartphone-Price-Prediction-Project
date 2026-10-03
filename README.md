# 📱 Smartphone Price Prediction System

An end-to-end machine learning system that predicts smartphone market prices in Indian Rupees (₹) using hardware, display, and camera specifications. Built from the ground up with a complete scikit-learn pipeline and deployed as an interactive Streamlit application.

---

## 📌 Project Highlights
- **Ground-Up Machine Learning Pipeline:** Integrated preprocessing, scaling, and regressor steps into a single reusable `Pipeline` object to ensure zero data leakage.
- **Skew-Handled Target Variable:** Handled the heavy right-skew of smartphone prices using logarithmic transformation (`np.log1p`), converting predictions back to actual currency via `np.expm1`.
- **Decoupled System Architecture:** Clean separation of exploratory code, automated inference (`prediction.py`), and interactive frontend presentation (`app.py`).
- **Interactive UI:** Built a responsive Streamlit application allowing users to simulate smartphone configurations and view real-time price predictions.

---

## 📊 Model Performance & Evaluation

The core estimator is an **XGBoost Regressor** evaluated on an unseen test set:

| Model | $R^2$ Score (Log Space) | Test MAE (True ₹) | Status |
| :--- | :---: | :---: | :---: |
| **XGBoost Regressor** | **0.8985** | **₹6,564** | **Production Model** |

> **Key Takeaway:** The final tuned XGBoost regressor explains **~89.9%** of market price variance, with an average absolute prediction error of **₹6,564** across diverse smartphone tiers.

---

## ⚙️ Machine Learning Pipeline Architecture

The inference flow uses Scikit-Learn's `ColumnTransformer` to handle different feature types:

1. **Numerical Features:** `Ram`, `Rom`, `Capacity`, `Watt`, `RearMP`, `FrontMP`, `Inches`, `Hz`, etc.
   - Handled via `SimpleImputer(strategy='median')` and `StandardScaler()`.
2. **Binary & Constant Features:** `5G`, `NFC`, `IrBlaster`, `FastCharging`, `HasMemoryCard`, `IsHybrid`, `ExtraSupport`.
   - Handled via `SimpleImputer(strategy='constant', fill_value=0)` and `StandardScaler()`.
3. **Categorical Features:** `Brand`, `OS`, `ProcessorName`, `Notches`.
   - Handled via `SimpleImputer(strategy='most_frequent')` and `OneHotEncoder(handle_unknown='ignore')`.
4. **Regressor:** `XGBRegressor` fitted on log-transformed targets.
5. **Artifact Storage:** Serialized pipeline saved to `models/smartphone_price_model.joblib`.

---

## 📁 Repository Structure

```text
├── data/
│   ├── raw/
│   │   └── smartphones - smartphones.csv      # Raw source data
│   └── processed/
│       └── cleaned_smartphones.csv            # Cleaned dataset for modeling
├── models/
│   └── smartphone_price_model.joblib          # Serialized production pipeline
├── notebooks/
│   ├── 01_data_understanding.ipynb            # Initial inspection & schema analysis
│   ├── 02_data_cleaning.ipynb                 # Missing value & string handling
│   ├── 03_eda.ipynb                           # Exploratory Data Analysis & visuals
│   ├── 04_feature_engineering.ipynb           # Encoders, scalers & model training
│   └── 05_model_prediction_testing.ipynb      # Model verification & sanity checks
├── app.py                                     # Streamlit user interface
├── prediction.py                              # Model loading & inference module
├── requirements.txt                           # Project dependencies
└── README.md                                  # Documentation
```
