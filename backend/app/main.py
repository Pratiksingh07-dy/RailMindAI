from fastapi import FastAPI
from app.routes import health, user, profile, report

from app.database.database import engine, Base
from app.models.user import User
from app.models.report import Report


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(health.router)
app.include_router(user.router)
app.include_router(profile.router)
app.include_router(report.router)

@app.get("/")
def home():
    return {"message": "RailMind AI Backend Running"}