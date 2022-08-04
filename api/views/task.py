import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django import forms
from api import models
from api.utils.BootStrap import BootStrapModelForm
from api.utils.pagenation import Pagenation


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        # widgets={
        #     "detail":forms.TextInput
        # }


def task_list(request):
    """任务列表"""
    #去数据库中获取所有任务
    queryset=models.Task.objects.all().order_by('-id')
    page_object=Pagenation(request,queryset)

    form = TaskModelForm()

    context={
        "form": form,
        "queryset":page_object.page_queryset,
        "page_string":page_object.html()
    }
    return render(request, 'task_list.html', context)


@csrf_exempt
def task_ajax(request):
    # print(request.GET)
    # print(request.POST)

    data_dict = {"status": True, "data": [11, 22, 33]}
    # return JsonResponse(data_dict)
    return HttpResponse(json.dumps(data_dict))


@csrf_exempt
def task_add(request):
    """添加任务"""
    # < QueryDict: {'level': ['1'], 'title': ['123'], 'detail': ['321312'], 'user': ['2']} >
    # print(request.POST)

    # 1.用户发送过来的数据进行校验（ModelForm校验）
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        # return JsonResponse(data_dict)
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status": False, "error": form.errors}
    # return JsonResponse(data_dict)
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
