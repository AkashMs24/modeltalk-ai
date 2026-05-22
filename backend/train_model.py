"""
Train the Loan Credit Risk Model using real Kaggle 'Give Me Some Credit' dataset.
Dataset: cs-training.csv from https://www.kaggle.com/c/GiveMeSomeCredit

Kaggle columns → app feature names:
  RevolvingUtilizationOfUnsecuredLines → revolving_utilization
  age                                  → age
  NumberOfTime30-59DaysPastDueNotWorse → times_30_59_days_late
  DebtRatio                            → debt_to_income_ratio
  MonthlyIncome                        → monthly_income
  NumberOfOpenCreditLinesAndLoans      → num_credit_lines
  NumberOfTimes90DaysLate              → times_90_days_late
  NumberRealEstateLoansOrLines         → num_real_estate_loans
  NumberOfTime60-89DaysPastDueNotWorse → times_60_89_days_late
  NumberOfDependents                   → num_dependents
  SeriousDlqin2yrs                     → default (label)
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.impute import SimpleImputer
import shap

SEED = 42
np.random.seed(SEED)

RAW_DATA_PATH = "cs-training.csv"
DATA_PATH     = "data/loan_data.csv"
MODEL_PATH    = "data/loan_model.joblib"
SCALER_PATH   = "data/scaler.joblib"
EXPLAINER_PATH= "data/shap_explainer.joblib"

os.makedirs("data", exist_ok=True)

# Maps Kaggle columns → your app's feature names
COLUMN_MAP = {
    "RevolvingUtilizationOfUnsecuredLines": "revolving_utilization",
    "age":                                   "age",
    "NumberOfTime30-59DaysPastDueNotWorse":  "times_30_59_days_late",
    "DebtRatio":                             "debt_to_income_ratio",
    "MonthlyIncome":                         "monthly_income",
    "NumberOfOpenCreditLinesAndLoans":       "num_credit_lines",
    "NumberOfTimes90DaysLate":               "times_90_days_late",
    "NumberRealEstateLoansOrLines":          "num_real_estate_loans",
    "NumberOfTime60-89DaysPastDueNotWorse":  "times_60_89_days_late",
    "NumberOfDependents":                    "num_dependents",
    "SeriousDlqin2yrs":                      "default",
}

FEATURE_COLS = [
    "revolving_utilization",
    "age",
    "times_30_59_days_late",
    "debt_to_income_ratio",
    "monthly_income",
    "num_credit_lines",
    "times_90_days_late",
    "num_real_estate_loans",
    "times_60_89_days_late",
    "num_dependents",
]


def load_and_clean(path: str) -> pd.DataFrame:
    print(f"Loading dataset from: {path}")
    df = pd.read_csv(path)

    # Drop the unnamed row-index column Kaggle adds
    df = df.drop(columns=[c for c in df.columns if c.lower().startswith("unnamed")], errors="ignore")

    # Rename columns
    df = df.rename(columns=COLUMN_MAP)

    # Keep only the columns we need
    needed = FEATURE_COLS + ["default"]
    df = df[[c for c in needed if c in df.columns]]

    print(f"Raw shape: {df.shape}  |  Default rate: {df['default'].mean():.2%}")

    # --- Data-quality fixes ---
    # Revolving utilization > 1 is usually data error; cap at 1
    df["revolving_utilization"] = df["revolving_utilization"].clip(0, 1)

    # DebtRatio outliers (e.g. 3000+) — cap at 5 (500%)
    df["debt_to_income_ratio"] = df["debt_to_income_ratio"].clip(0, 5)

    # Remove clearly invalid ages
    df = df[(df["age"] >= 18) & (df["age"] <= 100)]

    # Impute missing values (MonthlyIncome ~20% missing, NumberOfDependents ~2.5%)
    imputer = SimpleImputer(strategy="median")
    df[FEATURE_COLS] = imputer.fit_transform(df[FEATURE_COLS])

    print(f"Cleaned shape: {df.shape}")
    return df


def train():
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(
            f"'{RAW_DATA_PATH}' not found in the working directory.\n"
            "Download cs-training.csv from https://www.kaggle.com/c/GiveMeSomeCredit "
            "and place it in the backend/ folder."
        )

    df = load_and_clean(RAW_DATA_PATH)
    df.to_csv(DATA_PATH, index=False)
    print(f"Cleaned dataset saved → {DATA_PATH}")

    X = df[FEATURE_COLS]
    y = df["default"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEED, stratify=y
    )

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    print("Training Gradient Boosting model...")
    model = GradientBoostingClassifier(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        min_samples_leaf=20,
        random_state=SEED,
    )
    model.fit(X_train_sc, y_train)

    y_pred = model.predict(X_test_sc)
    y_prob = model.predict_proba(X_test_sc)[:, 1]
    auc = roc_auc_score(y_test, y_prob)
    print(f"\nAUC-ROC: {auc:.4f}")
    print(classification_report(y_test, y_pred, target_names=["Approved", "Rejected"]))

    print("Computing SHAP explainer...")
    # Use a background sample for speed (full dataset is 150k rows)
    background = shap.sample(X_train_sc, 500, random_state=SEED)
    explainer = shap.TreeExplainer(model, background)

    joblib.dump(model,    MODEL_PATH)
    joblib.dump(scaler,   SCALER_PATH)
    joblib.dump(explainer, EXPLAINER_PATH)

    print(f"\nAll artifacts saved.")
    print(f"  Model     → {MODEL_PATH}")
    print(f"  Scaler    → {SCALER_PATH}")
    print(f"  Explainer → {EXPLAINER_PATH}")
    print("\nTraining complete!")


if __name__ == "__main__":
    train()
