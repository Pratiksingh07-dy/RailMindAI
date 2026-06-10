from fastapi import FastAPI

from app.routes.user import router as user_router
from app.routes.report import router as report_router

app = FastAPI(
    title="RailMind AI Backend"
)

app.include_router(user_router)
app.include_router(report_router)

@app.get("/")
def home():
    return {
        "message": "RailMind AI Backend Running"
    }