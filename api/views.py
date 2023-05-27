from rest_framework.decorators import api_view, permission_classes,action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer,TagSerializer,MessageSerializer
from projects.models import Project, Review, Tag
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters,pagination

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


class TagsViewSet(ModelViewSet):
    queryset = Tag.objects.order_by('id')

    serializer_class = TagSerializer

    filter_backends=[DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]

    # filterset_fields = ['id', 'name']
    filterset_class = TagFilters

    search_fields=['name']

    ordering_fields = ['id','name']

    pagination_class = pagination.LimitOffsetPagination

    def list(self,request,*args,**kwargs):
        return super().list(request,*args,**kwargs)

    def create(self,request,*args,**kwargs):
        return super().create(request,*args,**kwargs)

    def update(self,request,*args,**kwargs):
        return super().update(request,*args,**kwargs)

    def partial_update(self,request,*args,**kwargs):
        return super().partial_update(request,*args,**kwargs)

    def destroy(self,request,*args,**kwargs):
        return super().destroy(request,*args,**kwargs)

    @action(detail=False,methods=['post'],url_path='test',serializer_class=MessageSerializer)
    def test(self,request,*args,**kwargs):
        return Response({
            'code':0,
            'message':'success'
        })



