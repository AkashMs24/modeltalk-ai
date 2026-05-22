"""
Train the Loan Credit Risk Model using real Kaggle 'Give Me Some Credit' dataset.
Dataset: cs-training.csv from https://www.kaggle.com/c/GiveMeSomeCredit
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

RAW_DATA_PATH = "data/cs-training.csv"
DATA_PATH     = "data/loan_data.csv"
MODEL_PATH    = "data/loan_model.joblib"
SCALER_PATH   = "data/scaler.joblib"
EXPLAINER_PATH= "data/shap_explainer.joblib"

os.makedirs("data", exist_ok=True)

# Maps Kaggle columns → your app's feature names
COLUMN_MAP = {
    "age":                                    "age",
    "MonthlyIncome":                          "annual_income",      # will multiply x12
    "RevolvingUtilizationOfUnsecuredLines":   "debt_to_income_ratio",
    "NumberOfOpenCreditLinesAndLoans":        "num_credit_lines",
    "NumberOfTimes90DaysLate":                "num_delinquencies",
    "DebtRatio":                              "loan_amount",        # proxy — see note
    "NumberOfTime30-59DaysPastDueNotWorse":   "employment_years",   # proxy — see note
    "SeriousDlqin2yrs":                       "default",
}

FEATURE_COLS = [
    "age", "annual_income", "debt_to_income_ratio",
    "num_credit_lines", "num_delinquencies",
    "loan_amount", "employment_years",
]


def load_and_clean():
    print("Loading real dataset...")
    df = pd.read_csv(RAW_DATA_PATH, index_col=0)
    print(f"Raw shape: {df.shape}")

    # Rename columns
    df = df.rename(columns={
        "SeriousDlqin2yrs":                       "default",
        "age":                                     "age",
        "MonthlyIncome":                           "monthly_income",
        "RevolvingUtilizationOfUnsecuredLines":    "debt_to_income_ratio",
        "NumberOfOpenCreditLinesAndLoans":         "num_credit_lines",
        "NumberOfTimes90DaysLate":                 "num_delinquencies",
        "DebtRatio":                               "loan_amount",
        "NumberOfTime30-59DaysPastDueNotWorse":    "employment_years",
    })

    # Convert monthly income to annual
    df["annual_income"] = df["monthly_income"] * 12

    # Cap extreme outliers
    df["debt_to_income_ratio"] = df["debt_to_income_ratio"].clip(0, 1)
    df["loan_amount"] = df["loan_amount"].clip(0, 5)
    df["num_delinquencies"] = df["num_delinquencies"].clip(0, 20)
    df["employment_years"] = df["employment_years"].clip(0, 20)
    df["age"] = df["age"].clip(18, 100)

    # Impute missing values with median
    imputer = SimpleImputer(strategy="median")
    df[FEATURE_COLS] = imputer.fit_transform(df[FEATURE_COLS])

    # Drop rows where target is missing
    df = df.dropna(subset=["default"])
    df["default"] = df["default"].astype(int)

    print(f"Cleaned shape: {df.shape}")
    print(f"Default rate: {df['default'].mean():.2%}")
    return df


def train():
    df = load_and_clean()
    df.to_csv(DATA_PATH, index=False)
    print(f"Saved cleaned data → {DATA_PATH}")

    X = df[FEATURE_COLS]
    y = df["default"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEED, stratify=y
    )

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    print("Training Gradient Boosting model on real data...")
    model = GradientBoostingClassifier(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        min_samples_leaf=50,
        random_state=SEED
    )
    model.fit(X_train_sc, y_train)

    y_pred = model.predict(X_test_sc)
    y_prob = model.predict_proba(X_test_sc)[:, 1]
    auc = roc_auc_score(y_test, y_prob)
    print(f"\nAUC-ROC: {auc:.4f}")
    print(classification_report(y_test, y_pred, target_names=["Approved", "Rejected"]))

    print("Computing SHAP explainer...")
    explainer = shap.TreeExplainer(model)

    joblib.dump(model,     MODEL_PATH)
    joblib.dump(scaler,    SCALER_PATH)
    joblib.dump(explainer, EXPLAINER_PATH)
    print("All artifacts saved. Training complete!")


if __name__ == "__main__":
    train()
