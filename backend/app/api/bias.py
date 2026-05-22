from fastapi import APIRouter
import numpy as np
import pandas as pd
from app.models.schemas import BiasReport
from app.core.model_loader import get_model, get_scaler, FEATURE_COLS

router = APIRouter()

DEMOGRAPHIC_COLS = ["gender", "ethnicity", "zip_region"]

SENSITIVE_GROUPS = {
    "gender": ["Female"],
    "ethnicity": ["Black", "Hispanic"],
    "zip_region": ["Rural"]
}


@router.get("/bias-report", response_model=BiasReport)
def bias_report():
    import os
    data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "loan_data.csv")
    df = pd.read_csv(data_path)

    model = get_model()
    scaler = get_scaler()

    X = df[FEATURE_COLS]
    X_sc = scaler.transform(X)
    df["predicted_approval"] = (model.predict_proba(X_sc)[:, 1] < 0.5).astype(int)

    demographic_breakdown = {}
    flagged_attributes = []
    disparate_impact = {}
    bias_scores = []

    for col in DEMOGRAPHIC_COLS:
        if col not in df.columns:
            continue

        group_rates = df.groupby(col)["predicted_approval"].mean().to_dict()
        demographic_breakdown[col] = {k: round(v, 4) for k, v in group_rates.items()}

        max_rate = max(group_rates.values())

        col_di = {}
        for group, rate in group_rates.items():
            di_ratio = rate / max_rate if max_rate > 0 else 1.0
            col_di[group] = round(di_ratio, 4)

            if group in SENSITIVE_GROUPS.get(col, []) and di_ratio < 0.8:
                flagged_attributes.append(f"{col}:{group} (DI={di_ratio:.2f})")
                bias_scores.append(1 - di_ratio)

        disparate_impact[col] = col_di

    overall_bias_score = round(float(np.mean(bias_scores)) if bias_scores else 0.0, 4)
    bias_detected = overall_bias_score > 0.05

    if bias_detected:
        recommendation = (
            f"Bias detected in {len(flagged_attributes)} demographic segments. "
            "Consider re-weighting training data, applying fairness constraints, "
            "or auditing feature selection to remove proxy variables."
        )
    else:
        recommendation = "No significant bias detected. Continue monitoring with new data."

    return BiasReport(
        bias_detected=bias_detected,
        overall_bias_score=overall_bias_score,
        disparate_impact=disparate_impact,
        demographic_breakdown=demographic_breakdown,
        flagged_attributes=flagged_attributes,
        recommendation=recommendation
    )
