from backend.app.api.resource import router as resources_router
from fastapi import FastAPI
from backend.app.api.resource_metric import router as resource_metrics_router
from backend.app.api.resource_health import router as resource_health_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CloudOps Manager",
    description="Cloud resource management and monitoring platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        "http://127.0.0.1:5176",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resources_router)
app.include_router(resource_metrics_router)
app.include_router(resource_health_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}