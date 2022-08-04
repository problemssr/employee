from django.shortcuts import render, HttpResponse, redirect
from api import models
from api.utils.pagenation import Pagenation
from api.utils.BootStrap import BootStrapModelForm
from django import forms
from django.core.validators import RegexValidator, ValidationError
from api.utils.form import UserModelForm,PrettyModelForm,PrettyEditModelForm

def depart_list(request):
    """ 部门列表 """

    # 在数据库中获取所有部门信息
    querySet = models.Department.objects.all()

    page_object=Pagenation(request,querySet,page_size=2)
    context={
        'depart': page_object.page_queryset,
        'page_string':page_object.html()
    }

    return render(request, 'depart_list.html', context)


def depart_add(request):
    """ 添加部门 """
    if request.method == "GET":
        return render(request, 'depart_add.html')
    else:
        # 获取用户post数据
        title = request.POST.get("title")
        # 保存数据库
        models.Department.objects.create(title=title)
        # 重定向回部门列表
        return redirect("/depart/list/")


def depart_delete(request):
    """ 删除部门 """
    # 获取ID
    nid = request.GET.get("nid")
    # 删除
    models.Department.objects.filter(id=nid).delete()
    # 重定向回部门列表
    return redirect("/depart/list/")


def depart_edit(request):
    """ 编辑部门 """
    # 根据nid获取数据
    nid = request.GET.get("nid")
    if request.method == "GET":
        rows = models.Department.objects.filter(id=nid).first()
        return render(request, "depart_edit.html", {"row": rows})

    else:
        # 获取用户提交的标题
        title = request.POST.get("title")
        # 根据ID找到数据库中数据并更新
        models.Department.objects.filter(id=nid).update(title=title)

        return redirect("/depart/list")