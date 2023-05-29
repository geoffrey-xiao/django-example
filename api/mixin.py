from .serializers import TagSerializer
from rest_framework import viewsets
from projects import models
# from .serializers import TagSerializer
from io import StringIO
from rest_framework import response
import csv


class TagCsvMixin(viewsets.GenericViewSet):

    def compare(self, request):
        queryset = models.Tag.objects.all()

        serializer = TagSerializer(queryset, many=True)

        if request.META.get('MEDIA_TYPE') == 'text/csv':
            data = StringIO()

            fieldnames = ['id', 'name', 'created']

            writer = csv.DictWriter(data, fieldnames=fieldnames)

            writer.writeheader()

            for tag in serializer.data:
                writer.writerow(tag)

            return response.Response(data.getvalue())

        else:

            return response.Response(serializer.data)
