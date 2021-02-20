# -*- coding: utf-8 -*-
__author__ = 'wuhai'
from rest_framework.pagination import PageNumberPagination
from .exceptions import ValidationError


def get_object(model, object_id=None, *args, **kwargs):
    """
    Get model object instance by object_id
    """
    try:
        if object_id:
            object_id = model._meta.pk.to_python(object_id)
            return model.objects.get(pk=object_id, **kwargs)
        else:
            return model.objects.get(**kwargs)
    except model.DoesNotExist:
        raise ValidationError("Matching query does not exist.")


class BasePagination(PageNumberPagination):
    """
    Base pagination setting
    """
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    # max_page_size = 100
