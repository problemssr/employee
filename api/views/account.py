from django.shortcuts import render, redirect, HttpResponse
from django import forms
from api import models
from api.utils.BootStrap import BootStrapForm
from api.utils.encrypt import md5
from api.utils.code import check_code


class LoginForm(BootStrapForm):
    # Form需要自定义手写所有字段
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


class LoginModelForm(forms.ModelForm):
    # ModelForm在数据库中直接拿字段
    class Meta:
        model = models.Admin
        fields = ["username", "password"]


def login(request):
    """登录"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # 验证成功后获取到的用户名和密码
            # print(form.cleaned_data)

            #验证码的校验
            user_input_code=form.cleaned_data.pop("code")
            code=request.session.get('image_code','')
            if code.upper()!=user_input_code.upper():
                form.add_error('code', "验证码错误")
                return render(request, 'login.html', {'form': form})

            # 数据库校验字段,获取用户对象
            # 1.admin_object=models.Admin.objects.filter(username=form.cleaned_data.get("username"),password=form.cleaned_data.get("password")).first()
            admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
            if not admin_object:
                # form.add_error("username","用户名或密码错误")
                form.add_error("password", "用户名或密码错误")
                return render(request, 'login.html', {'form': form})
            # 用户名和密码正确
            # 网站随机生成字符串：写到用户浏览器的cookie中，在写入到session
            request.session["info"] = {
                "id": admin_object.id,
                "username": admin_object.username
            }
            #session可以保存七天
            request.session.set_expiry(60*60*24*7)
            return redirect('/admin/list')
        return render(request, 'login.html', {'form': form})


def logout(request):
    """注销"""
    request.session.clear()

    return redirect('/login/')


from io import BytesIO


def image_code(request):
    """生成图片验证码"""
    # 调用pillow函数，生成图片
    img, code_str = check_code()
    # print(code_str)

    # 写入到session中（便于后续获取验证码在进行校验）
    request.session['image_code'] = code_str
    # 给session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())
