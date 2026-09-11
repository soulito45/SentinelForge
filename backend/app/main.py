from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.domains import router as domains_router
from backend.app.api.scans import router as scans_router
from backend.app.api.dashboard import router as dashboard_router

app = FastAPI(
    title="RYNEX",
    description="External Attack Surface Intelligence & Risk Monitoring Platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(domains_router)
app.include_router(scans_router)
app.include_router(dashboard_router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "RYNEX API",
    }
