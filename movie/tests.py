from django.test import TestCase, Client

from .models import Movie, Actor


class TestMovieViewSet(TestCase):
    def setUp(self) -> None:
        # self.actor = Actor.objects.create(
        #     name="Bob Den",
        #     birthdate="2016-01-02",
        #     gender="m"
        # )
        self.movie = Movie.objects.create(
            name="Secret",
            year="2016-01-02",
            genre="Drama",
            imdb=8.9,
            # actors=self.actor
        )
        self.client = Client()

    def test_get_all_movies(self):
        response = self.client.get('/movies/')
        data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertIsNotNone(data[0]["id"])
        self.assertEqual(data[0]["name"], "Secret")
        # self.assertEqual(data[0]["actor__name"], "Bob Den")

    def test_search(self):
        response = self.client.get('/movies/?search=Secret')
        data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertIsNotNone(data[0]["id"])
        self.assertEqual(data[0]["name"], "Secret")

    def test_ordering(self):
        response = self.client.get('/movies/?ordering=-imdb')
        data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertIsNotNone(data[0]["id"])
        self.assertEqual(data[0]["name"], "Secret")
