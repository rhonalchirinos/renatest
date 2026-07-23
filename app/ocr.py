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


KEYWORDS = ["SURNAME", "NAME", "OF. IDENT", "DOCUMENT", "CUIL", "FECHA DE RADICACION", "TRAMITE", "DOCUMENTO", "DOCUMENTO TRAMITE Nª"]


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

    print("=== TEXTOS ENCONTRADOS ===")
    for i, t in enumerate(resultados, 1):
        print(f"{i}: {t}")
    print("=== BUSCANDO KEYWORDS ===")
    upper_textos = [t.upper() for t in resultados]
    for kw in KEYWORDS:
        encontrado = any(kw in t for t in upper_textos)
        print(f"  {kw}: {'✓' if encontrado else '✗'}")

    return {"verificado": verificar(resultados)}
