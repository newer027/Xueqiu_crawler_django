# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):

    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args, **kwargs) #设定for_fields后,执行其他代码

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # 没有当前值
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    # 筛选和for_fields中字段相同的对象
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                # 最后一个对象的order+1
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(OrderField, self).pre_save(model_instance, add) #super的用法
