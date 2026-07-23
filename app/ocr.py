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


KEYWORDS = ["SURNAME", "NAME", "OF. IDENT", "DOCUMENT", "CUIL", "FECHA DE RADICACION"]


def verificar(textos):
    upper_textos = [linea.upper() for linea in textos]
    for kw in KEYWORDS:
        if not any(kw in linea for linea in upper_textos):
            return False
    return True


def procesar_imagen(image_bytes: bytes):
    import cv2
    import numpy as np

    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    if img is None:
        return None

    reader = _get_reader()
    resultados = reader.readtext(img, detail=0)

    return {"verificado": verificar(resultados)}
