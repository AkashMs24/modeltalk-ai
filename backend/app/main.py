from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import predict, explain, bias, appeal, chat
from app.core.model_loader import load_artifacts

app = FastAPI(
    title="Explainable AI Copilot — Loan Credit Risk",
    description="Enterprise-grade XAI system with bias detection and decision appeal.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    load_artifacts()

app.include_router(predict.router, prefix="/api/v1", tags=["Prediction"])
app.include_router(explain.router, prefix="/api/v1", tags=["Explanation"])
app.include_router(bias.router, prefix="/api/v1", tags=["Bias Detection"])
app.include_router(appeal.router, prefix="/api/v1", tags=["Decision Appeal"])
app.include_router(chat.router, prefix="/api/v1", tags=["AI Copilot Chat"])

@app.get("/")
def health():
    return {"status": "ok", "message": "XAI Copilot API is running"}
