from fastapi import FastAPI

from backend.app.api.domains import router as domains_router
from backend.app.api.scans import router as scans_router


app = FastAPI(
    title="SentinelForge",
    description="External Attack Surface Intelligence & Risk Monitoring Platform",
    version="0.1.0",
)

app.include_router(domains_router)
app.include_router(scans_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SentinelForge API",
    }
