from django.core.management import BaseCommand
import requests as rq
from movietut.models import Genre


class Command(BaseCommand):
    def handle(self, *args, **options):
        API_URI = "https://api.themoviedb.org/3/genre"
        API_KEY = "e7e2852e5b4d9cc2fccd5fb9858411d9"

        # movie
        data = rq.get(f"{API_URI}/movie/list?api_key={API_KEY}").json()
        for jgenre in data['genres']:
            genre, created = Genre.objects.get_or_create(
                id=jgenre['id'],
                name=jgenre['name'],
            )

        # tv
        data = rq.get(f"{API_URI}/tv/list?api_key={API_KEY}").json()
        for jgenre in data['genres']:
            genre, created = Genre.objects.get_or_create(
                id=jgenre['id'],
                name=jgenre['name'],
            )

        # movie, fr
        data = rq.get(f"{API_URI}/movie/list?api_key={API_KEY}&language=FR-fr").json()
        for jgenre in data['genres']:
            genre = Genre.objects.get(id=jgenre['id'])
            genre.name_fr = jgenre['name']
            genre.save()

        # tv, fr
        data = rq.get(f"{API_URI}/tv/list?api_key={API_KEY}&language=FR-fr").json()
        for jgenre in data['genres']:
            genre = Genre.objects.get(id=jgenre['id'])
            genre.name_fr = jgenre['name']
            genre.save()
