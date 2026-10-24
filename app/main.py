from fastapi import FastAPI
from app.api.route.incidents import router as incident_router

app = FastAPI(
    title = "GraphOps Copilot API",
    description="AI powered incident investigation and response system",
    version="1.0.0"
)

app.include_router(incident_router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service":"GraphOps Copilot API"
    }