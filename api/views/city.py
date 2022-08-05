from django.shortcuts import render,redirect

from api import models
from api.utils.BootStrap import BootStrapModelForm


def city_list(request):
    """城市列表"""
    data = models.City.objects.all()
    return render(request, 'city_list.html', {"city": data})


class CityModelForm(BootStrapModelForm):
    bootStrap_exclude_fields = ["img"]

    class Meta:
        model = models.City
        fields = "__all__"


def city_add(request):
    """新建城市"""
    title = "新建城市"

    if request.method == "GET":
        form = CityModelForm()
        return render(request, 'upload_modelform.html', {"form": form, "title": title})
    else:
        form = CityModelForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            # 对文件：自动保存（字段+上传路径写入数据库）
            form.save()
            return redirect("/city/list/")
        return render(request, 'upload_modelform.html', {"form": form, "title": title})
