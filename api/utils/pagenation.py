"""
自定义分页组件

在views函数中:
def pretty_list(request):

    # 1.根据需求筛选自己的数据
    # order_by("-id")-----desc order_by("id")------asc
    pretty_list = models.PrettyNum.objects.all().order_by("-level")

    # pretty_list = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    # 2.实例化分页对象
    page_project = Pagenation(request, pretty_list)

    context = {
        "pretty_list": page_project.page_queryset,  #分完页的数据
        "page_string": page_project.html()          # 生成页码
    }

    return render(request, 'pretty_list.html',context)

在HTML页面中

        {% for pretty in pretty_list %}
            <tr>
                <td>{{ pretty.id }}</td>
                <td>{{ pretty.modile }}</td>
                <td>{{ pretty.price }}</td>
                <td>{{ pretty.get_level_display }}</td>
                <td>{{ pretty.get_status_display }}</td>
                <td>
                    <a href="/pretty/edit/{{ pretty.id }}" class="btn btn-sm btn-primary">编辑</a>
                    <a href="/pretty/delete/{{ pretty.id }}" class="btn btn-sm btn-danger">删除</a>
                </td>
            </tr>
        {% endfor %}

        <ul class="pagination">
            {{ page_string }}
        </ul>

"""
from django.utils.safestring import mark_safe


class Pagenation(object):
    def __init__(self, request, queryset, page_size=10, para_param="page", plus=2):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据（根据这个数据给他进行分页处理）
        :param page_size: 每页显示多少条数据
        :param para_param: 在URL中传递获取分页的参数，例如：/pretty/list/?page=12
        :param plus: 显示当前页的 前或后几页（页码）
        """

        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        # 1.根据用户想访问的页码，计算出起止位置
        page = request.GET.get(para_param, "1")

        if page.isdecimal():
            page = int(page)
        else:
            # 页码设定
            page = 1

        self.para_param = para_param
        self.page = page
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        # 数据总条数
        total_count = queryset.count()
        total_page_count, divide = divmod(total_count, page_size)
        if divide:
            total_page_count += 1
        self.total_page_count = total_page_count

        self.plus = plus

    def html(self):
        page_str_list = []

        # 首页
        self.query_dict.setlist(self.para_param, [1])
        first = '<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(first)

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.para_param, [self.page - 1])
            pre = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.para_param, [1])
            pre = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(pre)

        # 计算上下翻页
        if self.total_page_count<=2*self.plus+1:
            #数据库数据较少
            start_page=1
            end_page=self.total_page_count
        else:
            # 数据库数据多情况
            # 当前页<plus-----极小值
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页+plus>总页面
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.para_param, [i])
            if i == self.page:
                element = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                element = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(element)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.para_param, [self.page + 1])
            next = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.para_param, [self.total_page_count])
            next = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(next)

        # 尾页
        self.query_dict.setlist(self.para_param, [self.total_page_count])
        last = '<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(last)

        # 跳转
        route_link = """
        <li style="display: inline-block;margin-left: 50px;">
            <form method="get">
                <div class="input-group" style="float:right;width: 150px;">
                    <input type="text" name="page" class="form-control" placeholder="页码">
                    <span class="input-group-btn">
                    <button class="btn btn-default" type="submit">跳转</button>
                  </span>
                </div>
            </form>
        </li>
        """
        page_str_list.append(route_link)

        page_string = mark_safe("".join(page_str_list))

        return page_string
