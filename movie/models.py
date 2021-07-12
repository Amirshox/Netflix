from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Actor(models.Model):
    GENDER = [
        ('m', 'Male'),
        ('f', 'Female')
    ]
    name = models.CharField(max_length=300)
    birthdate = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=300)
    year = models.DateField()
    imdb = models.FloatField(max_length=2)
    genre = models.CharField(max_length=100)
    actors = models.ManyToManyField(Actor)

    def __str__(self):
        return self.name


class Comment(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.movie_id.name}"
