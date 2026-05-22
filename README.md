<div align="center">

# 🧠 XAI Copilot — Explainable AI for Credit Risk

> **Business users can now understand every AI loan decision — in plain English.**

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-GitHub_Pages-6C63FF?style=for-the-badge)](https://YOUR_USERNAME.github.io/xai-copilot/)
[![Backend](https://img.shields.io/badge/⚡_API-Render-00D48A?style=for-the-badge)](https://xai-copilot-api.onrender.com)
[![License](https://img.shields.io/badge/License-MIT-FFB547?style=for-the-badge)](LICENSE)

</div>

---

## ✨ What Is This?

An **enterprise-grade Explainable AI system** for loan credit risk — combining:
- 🔍 **SHAP-powered explainability** — every decision is justified by specific data points
- ⚖️ **Bias detection** — disparate impact analysis across gender, ethnicity, and geography
- 🔄 **Decision appeal engine** — counterfactual analysis to flip rejections
- 💬 **AI Copilot chat** — plain-English Q&A powered by LLaMA 3 70B via Groq

---

## 🖼️ Features at a Glance

| Module | Description |
|---|---|
| **Predict & Explain** | Submit a loan application → instant decision + SHAP waterfall + LLM explanation |
| **Bias Detection** | Disparate impact ratios by gender, ethnicity, zip region. Flags groups below 80% threshold |
| **Decision Appeal** | Counterfactual analysis — finds minimal changes to flip rejection → approval |
| **AI Copilot Chat** | Ask anything about your decision in plain English via LLaMA 3 70B |

---

## 🏗️ Architecture
xai-copilot/
├── backend/                  # FastAPI + Python ML
│   ├── app/
│   │   ├── api/              # predict · explain · bias · appeal · chat
│   │   ├── core/             # Model loader singleton
│   │   ├── models/           # Pydantic schemas
│   │   └── services/         # Groq LLM integration
│   └── train_model.py        # Trains + saves ML artifacts
├── frontend/                 # React + Vite + Tailwind
│   └── src/
│       ├── pages/            # Dashboard · Predict · Bias · Appeal · Chat
│       ├── components/       # Layout + Sidebar
│       └── services/         # Axios API client
├── .github/workflows/        # GitHub Actions → auto deploy to Pages
└── render.yaml               # One-click Render deployment

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **ML Model** | Scikit-learn Gradient Boosting |
| **Explainability** | SHAP TreeExplainer |
| **Backend** | FastAPI + Uvicorn + Pydantic v2 |
| **LLM** | Groq API · LLaMA 3 70B (free tier) |
| **Frontend** | React 18 · Vite · Tailwind CSS · Recharts |
| **Deploy** | Render (backend) · GitHub Pages (frontend) |

---

## ⚡ Quick Start (Local)

### Prerequisites
- Python 3.10+
- Node.js 18+
- [Free Groq API Key](https://console.groq.com)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # Add your GROQ_API_KEY
python train_model.py          # Trains model + saves artifacts
uvicorn app.main:app --reload --port 8000
```
API docs → `http://localhost:8000/docs`

### Frontend
```bash
cd frontend
npm install
npm run dev
```
App → `http://localhost:5173`

---

## 🌐 Deploy (Free)

### Backend → Render
1. [render.com](https://render.com) → New Web Service → connect repo
2. Root Directory: `backend`
3. Build: `pip install -r requirements.txt && python train_model.py`
4. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add env var: `GROQ_API_KEY`

### Frontend → GitHub Pages
1. Repo Settings → Pages → Source: **GitHub Actions**
2. Add secret: `VITE_API_URL` = `https://your-backend.onrender.com/api/v1`
3. Push to `main` → auto deploys in ~2 min

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/predict` | Loan risk prediction |
| `POST` | `/api/v1/explain` | SHAP explanation + LLM summary |
| `GET` | `/api/v1/bias-report` | Full demographic bias report |
| `POST` | `/api/v1/appeal` | Decision appeal + counterfactuals |
| `POST` | `/api/v1/chat` | AI copilot chat |

---

## 🎯 Resume Highlights

- **XAI** — SHAP TreeExplainer for feature-level attributions on every prediction
- **Fairness** — Disparate impact analysis (80% rule) across 3 demographic axes
- **Counterfactuals** — Algorithmic engine finding minimal changes to flip decisions
- **RAG-style grounding** — LLM is grounded with SHAP values, no hallucination
- **Production-ready** — FastAPI async, Pydantic validation, CORS, singleton model loading
- **CI/CD** — GitHub Actions auto-deploys frontend on every push to main

---

<div align="center">

Made with ❤️ · MIT License

</div>
