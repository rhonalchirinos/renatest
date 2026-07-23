from fastapi import FastAPI
from pydantic import BaseModel
import base64

from .ocr import procesar_imagen

app = FastAPI(title="Renaper OCR API")


class ProcesarRequest(BaseModel):
    image_base64: str


class ProcesarResponse(BaseModel):
    texto: list[str]
    dni_encontrado: bool
    cuil_encontrado: bool


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/procesar", response_model=ProcesarResponse)
def procesar(req: ProcesarRequest):
    image_bytes = base64.b64decode(req.image_base64)
    resultado = procesar_imagen(image_bytes)
    if resultado is None:
        return {"error": "No se pudo decodificar la imagen"}
    return resultado
