from django.core.management import BaseCommand
import requests as rq
from movietut.models import Movie


class Command(BaseCommand):
    def handle(self, *args, **options):

        MIN_YEAR = 1885
        MAX_YEAR = 2021

        API_URI = "https://api.themoviedb.org/3/discover/movie"
        API_KEY = "e7e2852e5b4d9cc2fccd5fb9858411d9"

        for year in range(MIN_YEAR, MAX_YEAR + 1):
            print(year)
            data = rq.get(f"{API_URI}?api_key={API_KEY}&primary_release_year={year}").json()
            pages = int(data['total_pages'])

            for page in range(1, pages + 1):
                movies = rq.get(f"{API_URI}?api_key={API_KEY}&primary_release_year={year}&page={page}").json()

                for jmovie in movies['results']:
                    movie, created = Movie.objects.get_or_create(
                        id=jmovie['id'],
                        poster=jmovie['poster_path'],
                        adult=jmovie['adult'],
                        overview=jmovie['overview'],
                        release_date=jmovie['release_date'],
                        original_title=jmovie['original_title'],
                        original_language=jmovie['original_language'],
                        title=jmovie['title'],
                        popularity=jmovie['popularity'],
                        vote_count=jmovie['vote_count'],
                        vote_average=jmovie['vote_average'],
                    )
                    for jgenre in jmovie['genre_ids']:
                        movie.genres.add(jgenre)
                    movie.save()
