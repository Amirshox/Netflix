from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Movie, Actor, Comment
from .serializers import MovieSerializer, ActorSerializer, CommentSerializer


class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'actors__name']
    ordering_fields = ['imdb']
    filterset_fields = ['genre']

    # def get_queryset(self):
    #     queryset = Movie.objects.all()
    #     query = self.request.query_params.get('search')
    #     if query is not None:
    #         queryset = queryset.filter(name__icontains=query)
    #
    #     return queryset

    @action(detail=True, methods=['GET'])
    def actors(self, request, *args, **kwargs):
        movie = self.get_object()
        serializer = ActorSerializer(movie.actor.all(), many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["POST"], url_path='add-actor')
    def add_actor(self, request, pk, *args, **kwargs):
        movie = self.get_object()
        actor_id = request.data["actor_id"]
        actor = Actor.objects.get(pk=actor_id)
        movie.actors.add(actor)
        movie.save()
        return Response({'status': 'success'})

    @action(detail=True, methods=["DELETE"], url_path='remove-actor')
    def remove_actor(self, request, pk, *args, **kwargs):
        movie = self.get_object()
        actor_id = request.data["actor_id"]
        actor = Actor.objects.get(pk=actor_id)
        movie.actors.remove(actor)
        movie.save()
        return Response({'status': 'success'})


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Comment.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.validated_data["user_id"] = self.request.user
        serializer.save()
