
import django_filters.rest_framework as filters
from projects import models

class TagFilters(filters.FilterSet):
    # p_name 实际是查询`name`字段
    tag_name = filters.CharFilter(field_name='name',lookup_expr='icontains')

    class Meta:
        model = models.Tag
        # 对于`model`中存在的字段，可以直接指定字段名
        fields = ['id', 'name']
        # field = {
        #     'id':['contains','istarts'],
        #     'name':['contains','icontains','istarts']
        # }
        # 最终支持查询的字段包含自定义的`p_name`与  `fields`中指定的字段