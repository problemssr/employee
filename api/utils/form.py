from django.shortcuts import render, HttpResponse, redirect
from api import models
from api.utils.pagenation import Pagenation
from api.utils.BootStrap import BootStrapModelForm
from django import forms
from django.core.validators import RegexValidator, ValidationError

class UserModelForm(BootStrapModelForm):
    class Meta:
        model = models.UseInfo
        fields = ["name", "password", "age", "account", "create_time", "sex", "depart"]
        # 控制页面插件
        # widgets={
        #     # “name”想要修改页面的key attrs来添加
        #     "name":forms.TextInput(attrs={"class":"form-control"}),
        #     "password":forms.TextInput(attrs={"class":"form-control"}),
        #     "age":forms.TextInput(attrs={"class":"form-control"}),
        #     "account":forms.TextInput(attrs={"class":"form-control"}),
        # }

    # 获取页面字段(含义 自动通过循环找出所有字段的插件在绑定属性class)
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     # 循环找到所有插件，添加"class"="form-control"
    #     for name, field in self.fields.items():
    #         # 不加样式的办法
    #         # if name=="password":
    #         #     continue
    #         field.widget.attrs = {"class": "form-control", "placeholder": field.label}

class PrettyModelForm(BootStrapModelForm):
    modile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
    )

    class Meta:
        model = models.PrettyNum
        fields = ["modile", "price", "level", "status"]
        # fields = ["modile", "price", "level", "status"]-----自定义字段
        # fields = "__all__"--------全部字段
        # exclude=['level']---------去掉某字段

    # 调整样式
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     for name, field in self.fields.items():
    #         field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_modile(self):
        txt_mobile = self.cleaned_data["modile"]

        exist = models.PrettyNum.objects.filter(modile=txt_mobile).exists()
        if exist:
            raise ValidationError("手机号已存在")
        # if len(txt_mobile)!=11:
        #     #验证不通过
        #     raise ValidationError("输入格式错误")

        # 验证通过 用户输入值返回
        return txt_mobile

class PrettyEditModelForm(forms.ModelForm):
    # modile = forms.CharField(disabled=True, label="手机号")
    modile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
    )

    class Meta:
        model = models.PrettyNum
        fields = ["modile", "price", "level", "status"]
        # fields = ["modile", "price", "level", "status"]-----自定义字段
        # fields = "__all__"--------全部字段
        # exclude=['level']---------去掉某字段

    # 调整样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_modile(self):
        # 获取当前编辑行的id self.instance.pk
        # print(self.instance.pk)

        txt_mobile = self.cleaned_data["modile"]

        exist = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(modile=txt_mobile).exists()

        if exist:
            raise ValidationError("手机号已存在")
        # if len(txt_mobile)!=11:
        #     #验证不通过
        #     raise ValidationError("输入格式错误")

        # 验证通过 用户输入值返回
        return txt_mobile
