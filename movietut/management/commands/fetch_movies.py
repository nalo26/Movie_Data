from django.core.management import BaseCommand
import requests as rq


class Command(BaseCommand):
    def handle(self, *args, **options):

        MIN_YEAR = 1885
        MAX_YEAR = 2021

        API_URI = "https://api.themoviedb.org/3/discover/movie"
        API_KEY = "e7e2852e5b4d9cc2fccd5fb9858411d9"

            #for year in range(MIN_YEAR, MAX_YEAR + 1):
            #data = rq.get(f"{API_URI}?api_key={API_KEY}&primary_release_year={year}").json()
        data = rq.get(f"{API_URI}?api_key={API_KEY}&primary_release_year={2021}").json()
        pages = int(data['total_pages'])

        print(data)
            #for page in range(1, pages + 1):
            #    movies = rq.get(f"{API_URI}?api_key={API_KEY}&primary_release_year={year}&page={page}").json()
