from django.urls import path

from . import views                    # 같은 폴더의 views.py

urlpatterns = [
    path("hello/", views.hello, name="hello"),   # hello/ 주소 → 어떤 요리사?
    path("", views.index, name="index"),       # 빈 주소 = 첫 화면
]