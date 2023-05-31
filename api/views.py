from urllib.parse import urlencode
from django.urls import reverse
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer, TagSerializer, MessageSerializer
from projects.models import Project, Review, Tag
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, pagination

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.settings import api_settings

from .mixin import TagCsvMixin

from .renderer import TagRenderer

from .filters import TagFilters


@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/id/vote'},

        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]
    return Response(routes)


@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    review, created = Review.objects.get_or_create(
        owner=user,
        project=project,
    )

    review.value = data['value']
    review.save()
    project.getVoteCount

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
def removeTag(request):
    tagId = request.data['tag']
    projectId = request.data['project']

    project = Project.objects.get(id=projectId)
    tag = Tag.objects.get(id=tagId)

    project.tags.remove(tag)

    return Response('Tag was deleted!')


class TagsViewSet(ModelViewSet, TagCsvMixin):
    queryset = Tag.objects.all().order_by('id')

    serializer_class = TagSerializer

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    # filterset_fields = ['id', 'name']
    filterset_class = TagFilters

    search_fields = ['name']

    ordering_fields = ['id', 'name']

    pagination_class = pagination.LimitOffsetPagination

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['post'], url_path='test', serializer_class=MessageSerializer)
    def test(self, request, *args, **kwargs):
        return Response({
            'code': 0,
            'message': 'success'
        })

    @extend_schema(
        parameters=[OpenApiParameter(name='id', description='id', type=int),
                    OpenApiParameter(name='format', exclude=True)],
        responses={
            (200, 'application/json'): OpenApiResponse(TagSerializer(many=True)),
            (200, 'text/csv'): OpenApiTypes.BINARY
        })
    @action(detail=False, methods=['get'], url_path='test-csv',
            renderer_classes=(tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (TagRenderer,)))
    def test_csv(self, request):
        # return Response({'code':0})
        return super().compare(request)

    @action(detail=True, methods=['get'], url_path='test-tag')
    def test_tag(self, request, pk=None):
        tag = Tag.objects.get(id=pk)

        other_searilizer = TagSerializer(tag, many=False, context={
            'request': request, 'description': 'aaa'
        })

        return Response(other_searilizer.data)

    @extend_schema(responses=MessageSerializer,
                   parameters=[
                       OpenApiParameter(name='code', type=int,
                                        description='input code', required=True),
                       OpenApiParameter(name='message', type=str,
                                        description='input message', required=True)
                   ])
    @action(detail=True, methods=['get'], url_path='test-serializer', serializer_class=MessageSerializer)
    def test_serializer(self, request, **kwargs):
        tag = self.get_object()
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print('tag', tag)
        return Response(
            serializer.data,
            status=200
        )

    @extend_schema(exclude=True)
    @action(detail=True, methods=['get'], url_path='test-redirect')
    def test_redirect(self, request, **kwargs):
        params = request.query_params.dict()
        params.update(kwargs)

        return redirect(reverse('project-list') + '?' + urlencode(params))
