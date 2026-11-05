from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ecommerce-store REST API",
    description="Full-Stack E-Commerce Backend for ALTA Builder 30 (Track A)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to ecommerce-store API. Visit /docs for Swagger UI or /health for status."}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {
        "status": "OK",
        "database": "connected",
        "service": "ecommerce-store-backend"
    }
