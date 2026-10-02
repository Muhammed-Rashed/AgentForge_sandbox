from fastapi import FastAPI
from app.routers import auth

app = FastAPI(title="Backend Auth Service")

app.include_router(auth.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Auth service is running"}
