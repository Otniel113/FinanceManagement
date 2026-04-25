import os
import joblib
import pandas as pd
from decimal import Decimal
from typing import Dict

# Define Constants
INDUSTRY_AVERAGE_CRO = Decimal("0.12")

# Load Machine Learning Model
model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ml-models', 'lr2_final_model.pkl')
try:
    ml_model = joblib.load(model_path)
except Exception as e:
    print(f"Error loading ML model from {model_path}: {e}")
    ml_model = None

def decimal_to_display(value: Decimal, places: int = 4) -> str:
    """Format a Decimal value for display without converting through float."""
    quantizer = Decimal("1").scaleb(-places)
    return str(value.quantize(quantizer))

def build_result(cro: Decimal) -> Dict[str, str]:
    """Build the prediction result payload consumed by the view."""
    # 1. Simple Rule-Based Prediction
    rule_based_flexible = cro >= INDUSTRY_AVERAGE_CRO
    
    # 2. Logistic Regression Prediction
    lr_prob_str = "Tidak Tersedia"
    lr_flexible = False
    
    if ml_model is not None:
        # Prepare input for ML model
        X_input = pd.DataFrame({'CRO': [float(cro)]})
        predict_res = ml_model.predict(X_input)[0]
        predict_proba = ml_model.predict_proba(X_input)[0][1] # Probability of class 1 (Flexible)
        
        lr_flexible = (predict_res == 1)
        lr_prob_str = f"{predict_proba * 100:.2f}%"
    else:
        lr_flexible = rule_based_flexible

    srb_status = "Fleksibel" if rule_based_flexible else "Tidak Fleksibel"
    srb_color = "green" if rule_based_flexible else "red"
    lr_status = "Fleksibel" if lr_flexible else "Tidak Fleksibel"
    lr_color = "green" if lr_flexible else "red"

    description = (
        f"\n1. Prediksi Simple Rule-Based = <b style='color: {srb_color}'>{srb_status}</b>\n\n"
        f"2. Prediksi Regresi Logistik:\n"
        f"   a. Hasil = <b style='color: {lr_color}'>{lr_status}</b>\n"
        f"   b. Peluang = {lr_prob_str}"
    )

    if rule_based_flexible and lr_flexible:
        # Both are 1 (Flexible)
        return {
            "cro": decimal_to_display(cro),
            "ffr": "1 - Fleksibel",
            "title": "Perusahaan terindikasi fleksibel secara finansial",
            "description": description,
            "badge_class": "text-bg-success",
            "box_class": "result-flexible",
        }
    elif not rule_based_flexible and not lr_flexible:
        # Both are 0 (Not Flexible)
        return {
            "cro": decimal_to_display(cro),
            "ffr": "0 - Tidak Fleksibel",
            "title": "Perusahaan terindikasi belum fleksibel secara finansial",
            "description": description,
            "badge_class": "text-bg-danger",
            "box_class": "result-not-flexible",
        }
    else:
        # One is 1, One is 0
        return {
            "cro": decimal_to_display(cro),
            "ffr": "Mungkin Fleksibel",
            "title": "Perusahaan berpotensi fleksibel secara finansial",
            "description": description,
            "badge_class": "text-bg-warning",
            "box_class": "result-probably-flexible",
        }
