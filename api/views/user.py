from django.shortcuts import render, HttpResponse, redirect
from api import models
from api.utils.pagenation import Pagenation
from api.utils.BootStrap import BootStrapModelForm
from django import forms
from django.core.validators import RegexValidator, ValidationError
from api.utils.form import UserModelForm,PrettyModelForm,PrettyEditModelForm

def user_list(request):
    """用户管理"""
    # 获取数据库数据
    list = models.UseInfo.objects.all()
    # item.get_sex_display orm中有字段是元组内部套元组的格式----get_字段名_display

    page_object = Pagenation(request, list,page_size=2)
    context = {
        'info': page_object.page_queryset,
        'page_string': page_object.html()
    }

    return render(request, "user_list.html", context)


def user_add(request):
    """用户添加"""
    # 1.先看到用户添加页面
    context = {
        'sex_choices': models.UseInfo.sex_choices,
        'depart_list': models.Department.objects.all()
    }
    if request.method == "GET":
        return render(request, 'user_add.html', context)
    else:
        # 获取用户数据
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        age = request.POST.get("age")
        account = request.POST.get("account")
        create_time = request.POST.get("create_time")
        sex = request.POST.get("sex")
        depart = request.POST.get("depart")

        # 添加到数据库
        models.UseInfo.objects.create(name=user,
                                      password=pwd,
                                      age=age,
                                      account=account,
                                      create_time=create_time,
                                      sex=sex,
                                      depart_id=depart)
        # 返回用户列表页面
        return redirect('/user/list/')


"""""""""ModelForm示例"""""""""


def user_model_form_add(request):
    """ 添加用户（ModelForm版本）"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})
    # 用户提交数据
    else:
        form = UserModelForm(data=request.POST)
        if form.is_valid():
            # 校验成功
            # print(form.cleaned_data)#成功的数据
            form.save()
            return redirect('/user/list/')
            # return HttpResponse("插入成功")
        # 校验失败
        # print(form.errors)
        return render(request, "user_model_form_add.html", {"form": form})


def user_edit(request):
    """编辑用户"""
    nid = request.GET.get("nid")
    row = models.UseInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        # 根据ID去数据库获取要编辑的哪行数据
        form = UserModelForm(instance=row)
        return render(request, 'user_edit.html', {'form': form})

    else:
        # 根据ID找到数据库中数据并更新
        form = UserModelForm(data=request.POST, instance=row)
        if form.is_valid():
            # 默认保存是用户输入的所有数据，若想要用户在输入以外增加一点值
            # form.instance.字段名=值
            form.save()
            return redirect('/user/list')
        return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    models.UseInfo.objects.filter(id=nid).delete()
    return redirect('/user/list')