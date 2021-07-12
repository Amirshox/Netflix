from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Movie, Actor, Comment


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('name',)

    def validate_birthdate(value):
        if value.year < 1950:
            raise ValidationError(detail="Must be greater than 1950")
        return value


class MovieSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'movie_id', 'text')
