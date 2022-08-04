from django import forms


class BootStrap:
    # 获取页面字段(含义 自动通过循环找出所有字段的插件在绑定属性class)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有插件，添加"class"="form-control"
        for name, field in self.fields.items():
            # 不加样式的办法
            # if name=="password":
            #     continue
            # 字段中有属性，保留原来的属性，没有属性才增加
            # if field.widget.attrs:
            #     field.widget.attrs["class"]="form-control",
            #     field.widget.attrs["placeholder"]=field.label
            # else:
            field.widget.attrs = {
                "class": "form-control",
                "placeholder": field.label
            }


class BootStrapModelForm(BootStrap,forms.ModelForm):
    pass


class BootStrapForm(BootStrap,forms.Form):
    pass
