from django.db import models
import ast


class ListField(models.TextField):
    """自定义list字段
    models.SubfieldBase   提供to_python   和 from_db_value
    把数据库数据转化成python数据
    现在主要是from_db_value 方法 把数据库数据转化成python数据
    to_python 主要是接受form表单
    """
    # __metacalss__ = models.SubfieldBase
    description = 'Stores a python list'

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

        # def db_type(self, connection):
        #     if connection.setting_dict['ENGINE'] == 'django.db.backends.mysql':
        #         return 'listtype'

    def from_db_value(self, value, expression, connection, context):
        """数据库数据转成python数据"""

        if value is None:
            value = []
            return value
        if isinstance(value, list):
            return value
        return ast.literal_eval(value)

    def to_python(self, value):
        """从数据库中读取的数据转成python
        eval（value）读取value原来的类型
        ast模块就是帮助Python应用来处理抽象的语法解析的。
        而该模块下的literal_eval()函数：
        则会判断需要计算的内容计算后是不是合法的python类型，
        如果是则进行运算，否则就不进行运算。
        """
        if not value:
            value = []
        if isinstance(value, list):
            return value
        return ast.literal_eval(value)

    def get_prep_value(self, value):
        """
        把python数据压缩后保存到数据库
        或者说把python对象转化成查询值
        返回值是个字符串
        :param value:
        :return:
        """
        if value is None:
            return value
        return str(value)

    def get_prep_lookup(self, lookup_type, value):
        """限制查询方式"""
        if lookup_type == 'exact':
            return value
        elif lookup_type == 'in':
            return [self.get_prep_value(v) for v in value]
        else:
            return TypeError('lookup type %r not supported' % lookup_type)

    def value_to_string(self, obj):

        """转换字段数据以进行序列化
        Field._get_val_from_obj(obj) 是获取值序列化的最佳方式
        """
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
