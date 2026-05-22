from fastapi import APIRouter
import pandas as pd
from app.models.schemas import AppealRequest, AppealResult, LoanApplication
from app.core.model_loader import get_model, get_scaler, FEATURE_COLS
from app.services.groq_service import generate_appeal_response

router = APIRouter()


def _prob(data: dict, model, scaler) -> float:
    X = pd.DataFrame([{col: data[col] for col in FEATURE_COLS}])
    return float(model.predict_proba(scaler.transform(X))[0][1])


def _decision(prob: float) -> str:
    return "Rejected" if prob >= 0.5 else "Approved"


def find_counterfactuals(application: LoanApplication, model, scaler) -> list[dict]:
    base = {col: getattr(application, col) for col in FEATURE_COLS}
    base_prob = _prob(base, model, scaler)

    if base_prob < 0.5:
        return []   # Already approved

    suggestions = []

    # 1. Reduce revolving utilization
    for target in [0.5, 0.3, 0.1]:
        if target < application.revolving_utilization:
            test = {**base, "revolving_utilization": target}
            if _prob(test, model, scaler) < 0.5:
                suggestions.append({
                    "field":   "revolving_utilization",
                    "current": application.revolving_utilization,
                    "needed":  target,
                    "change":  f"Reduce credit utilization from {application.revolving_utilization:.0%} to {target:.0%}",
                    "impact":  "would flip to Approved",
                })
                break

    # 2. Clear late payments (30–59 days)
    if application.late_30_59_days > 0:
        test = {**base, "late_30_59_days": 0, "late_60_89_days": 0, "late_90_days": 0}
        if _prob(test, model, scaler) < 0.5:
            suggestions.append({
                "field":   "late_30_59_days",
                "current": application.late_30_59_days,
                "needed":  0,
                "change":  "Resolve all past-due accounts (30–90 day delinquencies cleared)",
                "impact":  "would flip to Approved",
            })

    # 3. Increase monthly income
    for mult in [1.2, 1.4, 1.6, 2.0]:
        new_income = round(application.monthly_income * mult)
        test = {**base, "monthly_income": new_income}
        if _prob(test, model, scaler) < 0.5:
            suggestions.append({
                "field":   "monthly_income",
                "current": application.monthly_income,
                "needed":  new_income,
                "change":  f"Increase monthly income to ${new_income:,.0f} ({int((mult-1)*100)}% increase)",
                "impact":  "would flip to Approved",
            })
            break

    # 4. Reduce debt ratio
    for target in [0.35, 0.25, 0.15]:
        if target < application.debt_ratio:
            test = {**base, "debt_ratio": target}
            if _prob(test, model, scaler) < 0.5:
                suggestions.append({
                    "field":   "debt_ratio",
                    "current": application.debt_ratio,
                    "needed":  target,
                    "change":  f"Reduce debt-to-income ratio from {application.debt_ratio:.2f} to {target:.2f}",
                    "impact":  "would flip to Approved",
                })
                break

    return suggestions


@router.post("/appeal", response_model=AppealResult)
async def appeal_decision(request: AppealRequest):
    model  = get_model()
    scaler = get_scaler()

    orig_data = {col: getattr(request.original_application, col) for col in FEATURE_COLS}
    orig_prob = _prob(orig_data, model, scaler)
    orig_dec  = _decision(orig_prob)

    # Apply any updated fields from appellant
    updated_data = {**orig_data}
    if request.updated_fields:
        for field, value in request.updated_fields.items():
            if field in updated_data:
                updated_data[field] = value

    appeal_prob = _prob(updated_data, model, scaler)
    appeal_dec  = _decision(appeal_prob)
    changed     = orig_dec != appeal_dec

    counterfactuals = find_counterfactuals(request.original_application, model, scaler)
    what_would_flip = [cf["change"] for cf in counterfactuals]

    improvement_suggestions = [
        "Pay down revolving credit balances to reduce utilization below 30%",
        "Bring all past-due accounts current and avoid new delinquencies",
        "Reduce total monthly debt obligations before reapplying",
        "Wait 6–12 months to establish a cleaner payment history",
        "Dispute any errors on your credit report with the credit bureaus",
    ]

    ai_response = await generate_appeal_response(
        original_application=request.original_application,
        appeal_reason=request.appeal_reason,
        original_decision=orig_dec,
        appeal_decision=appeal_dec,
        changed=changed,
        counterfactuals=counterfactuals,
    )

    return AppealResult(
        original_decision=orig_dec,
        appeal_decision=appeal_dec,
        changed=changed,
        improvement_suggestions=improvement_suggestions,
        what_would_flip_decision=what_would_flip,
        ai_response=ai_response,
    )
