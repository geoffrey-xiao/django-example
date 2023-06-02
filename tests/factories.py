
import factory
from projects import models


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tag
        django_get_or_create = ('name',)

    name = 'tag_test'
