import os
from django.shortcuts import render, HttpResponse, redirect
from django import forms
from api import models
from api.utils.BootStrap import BootStrapForm, BootStrapModelForm


def upload_list(request):
    """文件"""
    if request.method == "GET":
        return render(request, 'upload_list.html')
    # 'username': ['xina都是']
    # print(request.POST)  #    请求体数据
    # {'file': [ < TemporaryUploadedFile: IMG_20191004_180541.jpg(image / jpeg) >]}
    # print(request.FILES) #    请求发过来的文件

    file_obj = request.FILES.get("file")
    # print(file_obj.name) #获取文件名

    f = open(file_obj.name, mode='wb')
    for chunk in file_obj.chunks():
        # file_obj.chunks()一块一块文件
        f.write(chunk)
    f.close()

    return HttpResponse("....")


class UploadForm(BootStrapForm):
    bootStrap_exclude_fields = ["img"]
    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")


def upload_form(request):
    """Form上传"""
    title = "Form上传"
    if request.method == "GET":
        form = UploadForm()
        return render(request, 'upload_form.html', {"form": form, "title": title})

    form = UploadForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # {'name': '12', 'age': 111, 'img': < TemporaryUploadedFile: a1.png(image / png) >}
        # print(form.cleaned_data)
        from django.conf import settings
        # 自己读取数据，处理每个字段的数据
        # 1.读取图片内容，写入到文件夹中并获取文件的路径
        img_path = form.cleaned_data.get("img")
        # 数据库路径
        # db_path = os.path.join("static", "images", img_path.name)
        # media_path = os.path.join(settings.MEDIA_ROOT, img_path.name) 绝对路径
        media_path = os.path.join("media", img_path.name)
        # django最终文件路径
        # file_path = os.path.join("api", media_path)

        f = open(media_path, mode="wb")
        for chunk in img_path.chunks():
            f.write(chunk)
        f.close()
        # 2.将图片文件路径写入到数据库
        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=media_path
        )

        return HttpResponse("fsda")
    return render(request, 'upload_form.html', {"form": form, "title": title})


class UploadModelForm(BootStrapModelForm):
    bootStrap_exclude_fields = ["img"]

    class Meta:
        model = models.City
        fields = "__all__"


def upload_modelform(request):
    """ModelForm上传"""
    title = "ModelForm上传"

    if request.method == "GET":
        form = UploadModelForm()
        return render(request, 'upload_modelform.html', {"form": form, "title": title})
    else:
        form = UploadModelForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            # 对文件：自动保存（字段+上传路径写入数据库）
            form.save()
            return HttpResponse("ok")
        return render(request, 'upload_modelform.html', {"form": form, "title": title})
