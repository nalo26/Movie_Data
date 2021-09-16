from django.core.management import BaseCommand
import requests as rq
from movietut.models import Movie, Production_Country, Production_Company, Spoken_Languages


class Command(BaseCommand):
    def handle(self, *args, **options):
        API_URI = "https://api.themoviedb.org/3/movie/"
        API_KEY = "e7e2852e5b4d9cc2fccd5fb9858411d9"

        for movie in Movie.objects.all():
            data = rq.get(f"{API_URI}/{movie.id}?api_key={API_KEY}").json()

            movie.imbd_id = data['imdb_id']
            movie.budget = data['budget']
            movie.revenu = data['revenue']
            movie.runtime = data['runtime']
            movie.status = data['status']
            movie.tagline = data['tagline']

            for prod_count in data['production_countries']:
                obj, _ = Production_Country.objects.get_or_create(
                    iso = prod_count['iso_3166_1'],
                    name = prod_count['name']
                )
                movie.production_countries.add(obj)

            for prod_comp in data['production_companies']:
                obj, _ = Production_Company.objects.get_or_create(
                    id = prod_comp['id'],
                    logo = prod_comp['logo_path'],
                    name = prod_comp['name'],
                    origin_country = prod_comp['origin_country']
                )
                movie.production_companies.add(obj)

            for lang in data['spoken_languages']:
                obj, _ = Spoken_Languages.objects.get_or_create(
                    iso = lang['iso_639_1'],
                    name = lang['name']
                )
                movie.spoken_languages.add(obj)

            movie.save()
