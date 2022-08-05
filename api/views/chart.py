from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse


def chart_list(request):
    """数据统计列表"""
    return render(request, 'chart_list.html')


def chart_bar(request):
    """构造柱状图数据"""
    legend = ['销量', '业绩']
    data_xlist = ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
    data_list = [
        {
            "name": '销量',
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": '业绩',
            "type": 'bar',
            "data": [52, 23, 36, 30, 40, 20]
        },
    ]

    result = {
        "status": True,
        "data": {
            "legend": legend,
            "data_xlist": data_xlist,
            "data_list": data_list,
        }
    }

    return JsonResponse(result)


def chart_pie(request):
    """饼图数据"""
    db_data_list = [
        {"value": 1048, "name": 'IT'},
        {"value": 735, "name": '新媒体'},
        {"value": 1580, "name": '运营'},
        {"value": 2484, "name": '销售'},
    ]
    result = {
        "status": True,
        "data": db_data_list
    }
    return JsonResponse(result)


def chart_line(request):
    """折线数据"""
    legend = ['Email', 'Union Ads', 'Video Ads']
    xAxis = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    series_list = [
        {
            "name": 'Email',
            "type": 'line',
            "stack": 'Total',
            "data": [120, 132, 101, 134, 90, 230, 210]
        },
        {
            "name": 'Union Ads',
            "type": 'line',
            "stack": 'Total',
            "data": [220, 182, 191, 234, 290, 330, 310]
        },
        {
            "name": 'Video Ads',
            "type": 'line',
            "stack": 'Total',
            "data": [150, 232, 201, 154, 190, 330, 410]
        },
    ]
    result = {
        "status": True,
        "data": {
            "legend": legend,
            "xAxis": xAxis,
            "series_list": series_list
        }
    }
    return JsonResponse(result)

def highcharts(request):
    """highcharts实例"""
    return render(request,"highcharts.html")
