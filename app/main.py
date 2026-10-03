from fastapi import FastAPI
from app.routers import auth

app = FastAPI(title="Backend API", version="1.0.0")

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Service is running"}
