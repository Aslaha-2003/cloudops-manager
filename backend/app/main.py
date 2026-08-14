from fastapi import FastAPI

app = FastAPI(
    title="CloudOps Manager",
    description="Cloud resource management and monitoring platform",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}