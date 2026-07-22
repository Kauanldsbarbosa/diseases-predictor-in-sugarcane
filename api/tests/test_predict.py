import io
import pytest
from unittest.mock import MagicMock, patch
import numpy as np
from PIL import Image
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_predict_success(client: AsyncClient):
    # Criar uma imagem RGB fictícia 224x224 em memória
    img = Image.new("RGB", (224, 224), color="green")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="JPEG")
    img_bytes = img_byte_arr.getvalue()

    # Mock do modelo Keras retornando probabilidades fictícias
    mock_model = MagicMock()
    # 5 classes: Healthy, Mosaic, RedRot, Rust, Yellow
    mock_model.predict.return_value = np.array([[0.85, 0.05, 0.02, 0.03, 0.05]])

    with patch("app.endpoints.get_model", return_value=mock_model):
        files = {"file": ("leaf.jpg", img_bytes, "image/jpeg")}
        response = await client.post("/predict/", files=files)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["class_name"] == "Healthy"
        assert data["confidence"] == 0.85
        assert "probabilities" in data
        assert data["probabilities"]["Healthy"] == 0.85
        assert data["probabilities"]["Mosaic"] == 0.05


@pytest.mark.asyncio
async def test_predict_invalid_file_type(client: AsyncClient):
    files = {"file": ("test.txt", b"text content", "text/plain")}
    response = await client.post("/predict/", files=files)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "imagem válida" in response.json()["detail"]


@pytest.mark.asyncio
async def test_predict_corrupted_image(client: AsyncClient):
    files = {"file": ("bad_image.jpg", b"invalid image bytes", "image/jpeg")}
    response = await client.post("/predict/", files=files)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Erro ao processar imagem" in response.json()["detail"]
