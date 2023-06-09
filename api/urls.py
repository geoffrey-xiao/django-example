from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter
from .views import ProjectsViewSet, TagsViewSet
router = SimpleRouter()

router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'project-list', ProjectsViewSet, basename='project-list')
urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes),
    path('projects/', views.getProjects, name='project-list'),
    path('projects/<str:pk>/', views.getProject),
    path('projects/<str:pk>/vote/', views.projectVote),

    path('remove-tag/', views.removeTag),

    path('', include(router.urls))

]
