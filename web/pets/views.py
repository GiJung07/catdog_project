from django.http import HttpResponse
from django.shortcuts import render


def hello(request):                    # request = 손님의 주문서
    return HttpResponse("안녕하세요! 개냥 판별기예요 🐶🐱")

def index(request):
    context = {"title": "개냥 판별기", "message": "사진을 올리면 개인지 고양이인지 알려 드려요"}
    return render(request, "pets/index.html", context)    # 어떤 템플릿 파일에 담을까?