import cv2
import numpy as np
import requests

def _download_image(url: str) -> np.ndarray:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    img_bytes = np.asarray(bytearray(resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Nie udało się zdekodować obrazu")
    return img

def detect_people_from_url(url: str) -> int:
    img = _download_image(url)
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    rects, _ = hog.detectMultiScale(
        img,
        winStride=(4, 4),
        padding=(8, 8),
        scale=1.05,
    )
    return len(rects)
