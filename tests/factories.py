
import factory
from projects import models
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n+1)
    username = factory.LazyAttribute(lambda: f'user{id}')
    email = factory.LazyAttribute(lambda: f'{username}@email.com')


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tag
        django_get_or_create = ('name',)

    name = 'tag_test'
