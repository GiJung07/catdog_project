import base64
import io

from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image

from .forms import UploadForm
from .predict import predict            # Day 4에 만든 함수!


def hello(request):
    return HttpResponse("안녕하세요! 개냥 판별기예요 🐶🐱")

#첫 화면 = index 함수
def index(request):
    result = None
    if request.method == "POST":                         # 사진을 제출했을 때
        form = UploadForm(request.POST, request.FILES)    # 글자는 POST, 파일은 따로 들어와요
        if form.is_valid():                              # 검사 통과?
            upload = form.cleaned_data["image"]
            upload.seek(0)                               # 검사하느라 읽은 위치를 처음으로
            raw = upload.read()                          # 사진 파일 내용 (저장하지 않음)
            prob = predict(Image.open(io.BytesIO(raw)))  # {"고양이": 0.01, "개": 0.99}
            label = max(prob, key=prob.get)
            result = {
                "label": label,
                "cat": round(prob["고양이"] * 100),
                "dog": round(prob["개"] * 100),
                "sure": prob[label] >= 0.8,              # 80% 미만이면 "잘 모르겠어요"
                "image": f"data:{upload.content_type};base64,{base64.b64encode(raw).decode()}",
            }
    else:                                                # 처음 들어왔을 때 (GET)
        form = UploadForm()
    return render(request, "pets/index.html", {"title": "개냥 판별기", "form": form, "result": result})