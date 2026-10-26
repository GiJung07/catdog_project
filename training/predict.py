"""사진 한 장 → 개/고양이 확률. 웹사이트(Day 7)에서도 이 파일을 그대로 써요."""
from pathlib import Path

import numpy as np
import onnxruntime as ort
from PIL import Image

MODEL_PATH = Path(__file__).parent / "model.onnx"   # 이 파일과 같은 폴더의 model.onnx
RESIZE = 256                    # Day 2에서 메모한 resize_size
CROP = 224                      # Day 2에서 메모한 crop_size
MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)
LABELS = ["고양이", "개"]

_session = ort.InferenceSession(str(MODEL_PATH))   # 모델은 처음 한 번만 불러오기


def preprocess(img):
    img = img.convert("RGB")                       # 흑백·투명 PNG도 컬러 3장으로

    # ① 짧은 쪽을 RESIZE로 줄이기 (긴 쪽은 비율대로, 소수점 버림)
    w, h = img.size
    if w < h:
        size = (RESIZE, int(RESIZE * h / w))
    else:
        size = (int(RESIZE * w / h), RESIZE)
    img = img.resize(size, Image.BILINEAR)

    # ② 가운데 CROP × CROP 오리기
    w, h = img.size
    left, top = round((w - CROP) / 2), round((h - CROP) / 2)
    img = img.crop((left, top, left + CROP, top + CROP))

    # ③ 0~255 → 0~1 → 색 맞추기
    x = np.asarray(img, dtype=np.float32) / 255.0
    x = (x - MEAN) / STD

    # ④ (세로, 가로, 색) → (색, 세로, 가로), 그리고 1장짜리 묶음으로
    x = x.transpose(2, 0, 1)
    return x[None].astype(np.float32)


def predict(img):
    scores = _session.run(None, {"image": preprocess(img)})[0][0]   # 점수 2개
    prob = np.exp(scores - scores.max())
    prob = prob / prob.sum()                       # softmax: 점수 → 확률 (합계 1)
    return {name: float(p) for name, p in zip(LABELS, prob)}