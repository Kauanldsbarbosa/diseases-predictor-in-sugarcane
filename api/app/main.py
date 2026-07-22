from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.endpoints import router as predict_router

app = FastAPI(title="Sugarcane Disease Predictor API")

app.include_router(predict_router)


@app.get("/")
def index():
    return RedirectResponse(url="/docs")

