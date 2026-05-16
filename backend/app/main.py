from fastapi import FastAPI
from app.routes import health, user, profile

from app.database.database import engine, Base
from app.models.user import User


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(health.router)
app.include_router(user.router)
app.include_router(profile.router)

@app.get("/")
def home():
    return {"message": "RailMind AI Backend Running"}