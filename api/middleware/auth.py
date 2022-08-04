from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class Authmiddleware(MiddlewareMixin):
    """中间件1"""

    def process_request(self, request):
        # 0.排除不需要登录就可访问的页面
        # request.path_info-------获取当前用户请求url /login/
        if request.path_info in ["/login/","/image/code/"]:
            return

        # 1.读取当前访问用户的session信息，若能读到说明已登录过，继续向后走
        info_dict = request.session.get("info")
        if info_dict:
            # 若方法无返回值（返回None），言外之意可以继续走下一个中间件
            return
        else:
            # 2.没登录过，重回登录页面
            # 若有返回值,HttpResponse,render,言外之意就是走完这个中间件就结束了
            return redirect('/login/')

    def process_response(self, request, response):
        # print("M!走了")
        return response
