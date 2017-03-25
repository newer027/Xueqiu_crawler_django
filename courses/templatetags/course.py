# -*- coding: utf-8 -*-
from django import template


register = template.Library()


#_meta.model_name的用法
@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
