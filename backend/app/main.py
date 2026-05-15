from fastapi import FastAPI
from app.routes import health

from app.database.database import engine, Base
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(health.router)

@app.get("/")
def home():
    return {"message": "RailMind AI Backend Running"}