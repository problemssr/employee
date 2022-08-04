from django.shortcuts import render, HttpResponse, redirect
from api import models
from api.utils.pagenation import Pagenation
from api.utils.BootStrap import BootStrapModelForm
from django import forms
from django.core.validators import RegexValidator, ValidationError
from api.utils.form import UserModelForm, PrettyModelForm, PrettyEditModelForm


def pretty_list(request):
    """靓号列表"""

    # 搜索----start
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict = {"modile__contains": search_data}
    # res=models.PrettyNum.objects.filter(**data_dict)
    # print(res)
    # 搜索----end

    # order_by("-id")-----desc order_by("id")------asc
    # pretty_list = models.PrettyNum.objects.all().order_by("-level")

    pretty_list = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_project = Pagenation(request, pretty_list)

    context = {
        "pretty_list": page_project.page_queryset,
        "search_data": search_data,
        "page_string": page_project.html()
    }

    return render(request, 'pretty_list.html', context)


def pretty_add(request):
    """添加靓号"""
    if request.method == "GET":
        # 1.引入modelForm
        form = PrettyModelForm()
        # 2.渲染页面
        return render(request, "pretty_add.html", {"form": form})
    else:
        # 1.收集用户数据
        form = PrettyModelForm(data=request.POST)
        # 2.校验用户输入
        if form.is_valid():
            # 校验成功
            form.save()
            return redirect('/pretty/list/')
        # 校验失败
        return render(request, "pretty_add.html", {"form": form})


def pretty_edit(request, nid):
    """编辑靓号"""
    # -get1.根据id获取该行数据
    row = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        # -get2.将该行数据保存到modelform展示
        form = PrettyEditModelForm(instance=row)
        # -get2.页面返回数据信息
        return render(request, 'pretty_edit.html', {"form": form})
    else:
        # -post 1.根据ID找到数据库库中数据并更新(data=request.POST)
        form = PrettyEditModelForm(data=request.POST, instance=row)
        if form.is_valid():
            # -post 校验成功 保存数据
            form.save()
            # -post 重定向列表页
            return redirect('/pretty/list')
        # -post 校验失败回到该页面
        return render(request, 'pretty_edit.html', {"form": form})


def pretty_delete(request, nid):
    # 1.操作orm 删除数据最后重定向回去
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list')
