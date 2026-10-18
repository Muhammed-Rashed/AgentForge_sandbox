from fastapi import FastAPI
from app.routers import auth

app = FastAPI(title="Auth API")

app.include_router(auth.router, prefix="/api", tags=["auth"])


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Auth API service active"}
