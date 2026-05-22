import joblib
import os

_artifacts = {}

FEATURE_COLS = [
    "age", "annual_income", "loan_amount", "credit_score",
    "employment_years", "debt_to_income_ratio", "num_credit_lines",
    "num_delinquencies"
]

FEATURE_DESCRIPTIONS = {
    "age": "Applicant age in years",
    "annual_income": "Annual income in USD",
    "loan_amount": "Requested loan amount in USD",
    "credit_score": "Credit score (300–850)",
    "employment_years": "Years at current employer",
    "debt_to_income_ratio": "Total monthly debt / monthly income",
    "num_credit_lines": "Number of active credit lines",
    "num_delinquencies": "Number of past delinquencies"
}


def load_artifacts():
    base = os.path.join(os.path.dirname(__file__), "..", "..", "data")
    _artifacts["model"] = joblib.load(os.path.join(base, "loan_model.joblib"))
    _artifacts["scaler"] = joblib.load(os.path.join(base, "scaler.joblib"))
    _artifacts["explainer"] = joblib.load(os.path.join(base, "shap_explainer.joblib"))
    print("ML artifacts loaded successfully.")


def get_model():
    return _artifacts["model"]

def get_scaler():
    return _artifacts["scaler"]

def get_explainer():
    return _artifacts["explainer"]
