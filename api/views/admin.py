from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from api import models
from api.utils.encrypt import md5
from api.utils.pagenation import Pagenation


def admin_list(request):
    """管理员列表"""

    # 检查用户是否登录，登录进入主页面，未登录则跳回登录页面
    # 用户发来请求，获取cookie随机字符串，凭着该字符串比对session中是否存在
    # info = request.session.get("info")
    # print(info)

    # 构造搜索
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict = {"username__contains": search_data}
    # 根据搜索条件去数据库获取
    data = models.Admin.objects.filter(**data_dict)

    # 分页
    page_object = Pagenation(request, queryset=data)
    context = {
        'data': page_object.page_queryset,
        'page_string': page_object.html(),
        'search_data': search_data
    }

    return render(request, 'admin_list.html', context)


from django import forms
from api.utils.BootStrap import BootStrapModelForm


class AdminModelForm(BootStrapModelForm):
    # 自定义字段
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput()
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    # 密码
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)
        # 去数据库校验当前密码和新输入密码是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("密码不能和上一次一致")
        else:
            return md5(pwd)

    # 确认密码
    def clean_confirm_password(self):
        print(self.cleaned_data)
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        # 检查密码是否一致
        if pwd != confirm:
            raise ValidationError("密码不一致")
        # return回来的值才保存在数据库
        return confirm


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]


class AdminResetModelForm(BootStrapModelForm):
    # 自定义字段
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput()
    )

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    # 密码
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    # 确认密码
    def clean_confirm_password(self):
        print(self.cleaned_data)
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("密码不一致")
        # return回来的值才保存在数据库
        return confirm


def admin_add(request):
    """添加管理员"""
    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})
    else:
        form = AdminModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')
        return render(request, 'change.html', {'form': form, "title": title})


def admin_edit(request, nid):
    """编辑管理员"""
    # 对象/None
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        # return render(request, 'error.html', {"msg": '数据不存在'})
        return redirect('/admin/list/')
    title = "编辑管理员"

    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'change.html', {'form': form, 'title': title})
    else:
        form = AdminEditModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')

        return render(request, 'change.html', {'form': form, 'title': title})


def admin_delete(request, nid):
    """删除管理员"""
    models.Admin.objects.filter(id=nid).delete()

    return redirect('/admin/list/')


def admin_reset(request, nid):
    """重置密码"""
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')
    title = "重置密码----{}".format(row_object.username)
    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})
    else:
        # 表单验证
        form = AdminResetModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')

        return render(request, 'change.html', {'form': form, 'title': title})
