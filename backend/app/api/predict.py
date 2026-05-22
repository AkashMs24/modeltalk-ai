from fastapi import APIRouter
import pandas as pd
from app.models.schemas import LoanApplication, PredictionResult
from app.core.model_loader import get_model, get_scaler, FEATURE_COLS

router = APIRouter()


def build_features(application: LoanApplication) -> pd.DataFrame:
    return pd.DataFrame([{col: getattr(application, col) for col in FEATURE_COLS}])


def score(application: LoanApplication) -> tuple[str, float, float, str]:
    """Returns (decision, prob_default, risk_score, confidence)."""
    model  = get_model()
    scaler = get_scaler()
    X_sc   = scaler.transform(build_features(application))
    prob   = float(model.predict_proba(X_sc)[0][1])
    risk   = round(prob * 100, 1)
    dec    = "Rejected" if prob >= 0.5 else "Approved"
    conf   = "High" if prob < 0.25 or prob > 0.75 else "Medium"
    return dec, prob, risk, conf


@router.post("/predict", response_model=PredictionResult)
def predict(application: LoanApplication):
    model  = get_model()
    scaler = get_scaler()

    X_sc = scaler.transform(build_features(application))
    prob = float(model.predict_proba(X_sc)[0][1])

    decision   = "Rejected" if prob >= 0.5 else "Approved"
    risk_score = round(prob * 100, 1)
    confidence = "High" if prob < 0.25 or prob > 0.75 else "Medium"

    importances = model.feature_importances_
    top_factors = sorted(
        [{"feature": f, "importance": round(float(i), 4)}
         for f, i in zip(FEATURE_COLS, importances)],
        key=lambda x: x["importance"], reverse=True
    )[:5]

    return PredictionResult(
        decision=decision,
        probability_default=round(prob, 4),
        risk_score=risk_score,
        confidence=confidence,
        top_factors=top_factors,
    )
