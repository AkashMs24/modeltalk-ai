from fastapi import APIRouter
import numpy as np
import pandas as pd
from app.models.schemas import LoanApplication, ShapExplanation
from app.core.model_loader import get_model, get_scaler, get_explainer, FEATURE_COLS
from app.services.groq_service import generate_explanation

router = APIRouter()


def build_features(application: LoanApplication) -> pd.DataFrame:
    data = {col: getattr(application, col) for col in FEATURE_COLS}
    return pd.DataFrame([data])


@router.post("/explain", response_model=ShapExplanation)
async def explain(application: LoanApplication):
    model = get_model()
    scaler = get_scaler()
    explainer = get_explainer()

    X = build_features(application)
    X_sc = scaler.transform(X)

    shap_vals = explainer.shap_values(X_sc)[0]
    base_val = float(explainer.expected_value)
    prob_default = model.predict_proba(X_sc)[0][1]
    decision = "Rejected" if prob_default >= 0.5 else "Approved"
    risk_score = round(prob_default * 100, 1)

    shap_dict = {f: round(float(v), 4) for f, v in zip(FEATURE_COLS, shap_vals)}

    contributions = sorted(
        [
            {
                "feature": f,
                "value": getattr(application, f),
                "shap_value": shap_dict[f],
                "direction": "increases_risk" if shap_dict[f] > 0 else "decreases_risk",
                "magnitude": abs(shap_dict[f])
            }
            for f in FEATURE_COLS
        ],
        key=lambda x: x["magnitude"], reverse=True
    )

    plain_english = await generate_explanation(
        application=application,
        shap_contributions=contributions,
        decision=decision,
        risk_score=risk_score
    )

    return ShapExplanation(
        decision=decision,
        risk_score=risk_score,
        shap_values=shap_dict,
        base_value=base_val,
        plain_english=plain_english,
        feature_contributions=contributions
    )
