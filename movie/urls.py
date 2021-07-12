from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import MovieViewSet, ActorViewSet, CommentViewSet

router = DefaultRouter()
router.register('movies', MovieViewSet)
router.register('actors', ActorViewSet)
router.register('comments', CommentViewSet, 'comment')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', obtain_auth_token)
]
