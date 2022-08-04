from django.db import models


# Create your models here.
class Department(models.Model):
    """ 部门表 """
    # id=models.BigAutoField(verbose_name='ID',primary_key=True)
    title = models.CharField(verbose_name='标题', max_length=32)

    def __str__(self):
        return self.title


class UseInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=16)  # 字符字段
    password = models.CharField(verbose_name="密码", max_length=64)  # 字符字段
    age = models.IntegerField(verbose_name="年龄")  # 数字字段
    # verbose_name="账户余额"（备注信息）,max_digits=10（最大长度）,decimal_places=2（小数点后几位）,default=0（默认值）
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)  # 小数字段
    # create_time = models.DateTimeField(verbose_name="入职时间")
    create_time = models.DateField(verbose_name="入职时间")

    # 无约束
    # depart_id = models.BigIntegerField(verbose_name="部门ID")
    # 1.有约束
    # models.ForeignKey(to="Department", to_field="id")
    # -to，与那张表关联  -to_field，表中那一列关联
    # 2.django自动化 含义(depart = models.ForeignKey(to="Department", to_field="id")
    #   -写的depart
    #   -生成数据列 depart_id
    # 3.若部门表被删除
    #  3.1 级联删除
    # item.depart.title 取外键的字段值
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)
    #  3.2 置空
    # depart = models.ForeignKey(to="Department", to_field="id",on_delete=models.SET_NULL,null=True,blank=True)

    # django内部约束 固定数据 eg.性别（二值）
    sex_choices = (
        (1, "男"),
        (2, "女")
    )
    sex = models.SmallIntegerField(verbose_name="性别", choices=sex_choices)


class PrettyNum(models.Model):
    """靓号表"""
    modile = models.CharField(verbose_name="手机号", max_length=11)
    # 想要允许为空 null=True,blank=True
    price = models.IntegerField(verbose_name="价格")

    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)

    status_choices = (
        (1, "已占用"),
        (2, "未占用")
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)


class Admin(models.Model):
    ''' 管理员 '''
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username


class Task(models.Model):
    """任务表"""
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "临时"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详细信息")

    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)


class Order(models.Model):
    """订单"""
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")
    status_choices = (
        (1, "待支付"),
        (2, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    admin = models.ForeignKey(verbose_name="管理员", to="Admin", on_delete=models.CASCADE)
