<div align="center">

# 🤖 XAI Copilot
### Explainable AI for Loan Credit Risk

*SHAP-powered decisions · Bias detection · LLM copilot in plain English*

[![Live App](https://img.shields.io/badge/🌐_Live_App-xai--copilot.vercel.app-blue?style=for-the-badge)](https://xai-copilot.vercel.app)
[![API Docs](https://img.shields.io/badge/📄_API_Docs-Swagger_UI-green?style=for-the-badge)](https://xai-copilot-2.onrender.com/docs)
[![Backend](https://img.shields.io/badge/⚙️_Backend-onrender.com-orange?style=for-the-badge)](https://xai-copilot-2.onrender.com)

---

</div>

## ✨ Features

| Feature | Description |
|---|---|
| 📊 **Predict & Explain** | Submit a loan application, get an AI decision with SHAP feature impact chart |
| 🛡️ **Bias Detection** | Analyze model fairness across gender, ethnicity, and zip region |
| 📋 **Decision Appeal** | Appeal a rejection with counterfactual analysis — see what would flip the decision |
| 💬 **AI Copilot Chat** | Ask anything in plain English, powered by LLaMA 3.3 70B via Groq |

---

## 🛠️ Tech Stack

**Frontend** — React · Vite · Tailwind CSS · Recharts · Deployed on Vercel

**Backend** — FastAPI · Python 3.11 · scikit-learn · SHAP · Groq API · Deployed on Render

---

## 🚀 Run Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
python train_model.py        # generates ML artifacts
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables
```env
# frontend/.env
VITE_API_URL=http://localhost:8000/api/v1

# backend/.env
GROQ_API_KEY=gsk_...
```

---

## 🌐 Deployment

### Backend — Render
| Setting | Value |
|---|---|
| Runtime | Python 3.11.9 |
| Build Command | `pip install -r requirements.txt && python train_model.py` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| `PYTHON_VERSION` | `3.11.9` |
| `GROQ_API_KEY` | `gsk_...` |

### Frontend — Vercel
| Setting | Value |
|---|---|
| Root Directory | `frontend` |
| Framework | Vite |
| `VITE_API_URL` | `https://xai-copilot-2.onrender.com/api/v1` |

---

## 📁 Project Structure

```
XAi-copilot/
├── frontend/
│   ├── src/
│   │   ├── pages/        # Dashboard, Predict, Bias, Appeal, Copilot
│   │   ├── components/
│   │   └── services/     # API calls
│   └── vercel.json       # SPA routing config
├── backend/
│   ├── app/
│   │   ├── api/          # predict, explain, bias, appeal, chat
│   │   ├── core/         # model loader
│   │   ├── models/       # schemas
│   │   └── services/     # groq_service
│   ├── train_model.py    # trains model & saves artifacts
│   └── requirements.txt
└── render.yaml
```

---

## 🧠 ML Model

- **Algorithm** — Gradient Boosting Classifier (200 estimators, max depth 4)
- **Features** — Age, Annual Income, Loan Amount, Credit Score, Employment Years, Debt-to-Income Ratio, Credit Lines, Delinquencies
- **Explainability** — SHAP TreeExplainer
- **Training Data** — 3,000 synthetic loan applications with realistic demographic bias patterns

---

<div align="center">

MIT License · Built by [AkashMs24](https://github.com/AkashMs24)

</div>
