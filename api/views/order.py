import json
import random
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api import models
from api.utils.BootStrap import BootStrapModelForm
from api.utils.pagenation import Pagenation


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["oid", "admin"]


def order_list(request):
    """订单列表"""
    queryset = models.Order.objects.all().order_by('-id')
    page = Pagenation(request, queryset)
    form = OrderModelForm()
    context = {
        'form': form,
        "queryset": page.page_queryset,
        "page_string": page.html()
    }
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """新建订单（Ajax）"""
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 订单号：额外增加不是用户输入值的场景：动态计算
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        # 固定设置管理员ID------session中获取
        # form.instance.admin_id=当前登录系统管理员的ID
        form.instance.admin_id = request.session['info']['id']
        form.save()
        # return HttpResponse(json.dumps({"status":True}))
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "errors": form.errors})


def order_delete(request):
    """删除订单"""
    uid = request.GET.get("uid")
    exist = models.Order.objects.filter(id=uid).exists()
    if not exist:
        return JsonResponse({"status": False, 'error': '删除失败，数据不存在'})
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def order_detail(request):
    """通过id获取当前行数据"""
    """
    uid = request.GET.get("uid")
    row = models.Order.objects.filter(id=uid).first()
    if not row:
        return JsonResponse({"status": False, 'error': "编辑失败，数据不存在"})
    #从数据库获取一个对象---row
    result={
        "status":True,
        "data":{
            "title":row.title,
            "price":row.price,
            "status":row.status,
        }
    }
    return JsonResponse({"status":True,"data":result})
    """
    uid = request.GET.get("uid")
    row = models.Order.objects.filter(id=uid).values('title', 'price', 'status').first()
    if not row:
        return JsonResponse({"status": False, 'error': "编辑失败，数据不存在"})
    # 从数据库获取一个对象---row
    result = {
        "status": True,
        "data": row
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    """编辑订单"""
    uid = request.GET.get("uid")
    row = models.Order.objects.filter(id=uid).first()
    if not row:
        return JsonResponse({"status": False, 'tips': "编辑失败，数据不存在"})
    form = OrderModelForm(data=request.POST, instance=row)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})
