import ssl
import certifi

ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

_reader = None


def _get_reader():
    global _reader
    if _reader is None:
        import easyocr
        _reader = easyocr.Reader(['es'])
    return _reader


def buscar_dni(textos):
    for linea in textos:
        if "DNI" in linea.upper():
            return True
    return False


def buscar_cuil(textos):
    for linea in textos:
        if "CUIL" in linea.upper():
            return True
    return False


def procesar_imagen(image_bytes: bytes):
    import cv2
    import numpy as np

    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    if img is None:
        return None

    reader = _get_reader()
    resultados = reader.readtext(img, detail=0)

    return {
        "texto": resultados,
        "dni_encontrado": buscar_dni(resultados),
        "cuil_encontrado": buscar_cuil(resultados),
    }
