from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth

app = FastAPI(title="Auth API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api", tags=["auth"])


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Auth API service active"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
