import io
import os
from typing import Dict

import numpy as np
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from PIL import Image
from pydantic import BaseModel

router = APIRouter(prefix="/predict", tags=["Prediction"])

CLASS_NAMES = ["Healthy", "Mosaic", "RedRot", "Rust", "Yellow"]
MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "sugarcane_model_v1.keras"
)

_model = None


def get_model():
    global _model
    if _model is None:
        import keras

        if not os.path.exists(MODEL_PATH):
            raise RuntimeError(f"Modelo não encontrado no caminho: {MODEL_PATH}")
        _model = keras.models.load_model(MODEL_PATH)
    return _model


class PredictionResponse(BaseModel):
    class_name: str
    confidence: float
    probabilities: Dict[str, float]


@router.post("/", response_model=PredictionResponse, status_code=status.HTTP_200_OK)
async def predict(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O arquivo enviado deve ser uma imagem válida.",
        )

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image = image.resize((224, 224))
        img_array = np.array(image, dtype=np.float32)
        img_array = np.expand_dims(img_array, axis=0)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao processar imagem: {str(e)}",
        )

    try:
        model = get_model()
        preds = model.predict(img_array, verbose=0)[0]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro durante a predição do modelo: {str(e)}",
        )

    probabilities = {
        CLASS_NAMES[i]: float(preds[i]) for i in range(len(CLASS_NAMES))
    }
    top_index = int(np.argmax(preds))
    top_class = CLASS_NAMES[top_index]
    confidence = float(preds[top_index])

    return PredictionResponse(
        class_name=top_class,
        confidence=confidence,
        probabilities=probabilities,
    )
