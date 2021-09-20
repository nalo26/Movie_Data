from django.core.management import BaseCommand
import requests as rq
from movietut.models import Movie, Production_Country, Production_Company, Spoken_Languages
from tqdm import tqdm


class Command(BaseCommand):
    def handle(self, *args, **options):
        API_URI = "https://api.themoviedb.org/3/movie/"
        API_KEY = "e7e2852e5b4d9cc2fccd5fb9858411d9"

        for movie in tqdm(Movie.objects.all()):
            data = rq.get(f"{API_URI}/{movie.id}?api_key={API_KEY}").json()

            movie.imbd_id = data.get('imdb_id') if data.get('imdb_id') is not None else ""
            movie.budget = data.get('budget') if data.get('budget') is not None else 0
            movie.revenue = data.get('revenue') if data.get('revenue') is not None else 0
            movie.runtime = data.get('runtime') if data.get('runtime') is not None else 0
            movie.status = data.get('status') if data.get('status') is not None else ""
            movie.tagline = data.get('tagline') if data.get('tagline') is not None else ""

            production_countries = data.get('production_countries')
            if production_countries is not None:
                for prod_count in production_countries:
                    obj, _ = Production_Country.objects.get_or_create(
                        iso = prod_count.get('iso_3166_1'),
                        name = prod_count.get('name') if prod_count.get('name') is not None else ""
                    )
                    movie.production_countries.add(obj)

            production_companies = data.get('production_companies')
            if production_companies is not None:
                for prod_comp in production_companies:
                    obj, _ = Production_Company.objects.get_or_create(
                        id = prod_comp.get('id'),
                        logo = prod_comp.get('logo_path') if prod_comp.get('logo_path') is not None else "",
                        name = prod_comp.get('name') if prod_comp.get('name') is not None else "",
                        origin_country = prod_comp.get('origin_country') if prod_comp.get('origin_country') is not None else ""
                    )
                    movie.production_companies.add(obj)

            spoken_languages = data.get('spoken_languages')
            if spoken_languages is not None:
                for lang in data['spoken_languages']:
                    obj, _ = Spoken_Languages.objects.get_or_create(
                        iso = lang.get('iso_639_1'),
                        name = lang.get('name')
                    )
                    movie.spoken_languages.add(obj)

            movie.save()
