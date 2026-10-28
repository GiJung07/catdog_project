from django import forms


class UploadForm(forms.Form):
    image = forms.ImageField(label="사진")    # 사진 파일만 받는 칸