from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "RailMind AI Backend Running"}