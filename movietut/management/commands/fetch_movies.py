from django.core.management import BaseCommand
import requests as rq
from movietut.models import Movie, Production_Country, Production_Company, Spoken_Languages
from tqdm import tqdm


class Command(BaseCommand):
    def handle(self, *args, **options):

        # MIN_YEAR = 1885
        MIN_YEAR = 2021
        MAX_YEAR = 2021

        API_URI = "https://api.themoviedb.org/3"
        API_KEY = "e7e2852e5b4d9cc2fccd5fb9858411d9"
        current_id = -1
        try:
            for year in range(MIN_YEAR, MAX_YEAR + 1):
                print(year)
                data = rq.get(f"{API_URI}/discover/movie?api_key={API_KEY}&primary_release_year={year}").json()
                pages = int(data['total_pages'])

                for page in tqdm(range(1, pages + 1)):
                    movies = rq.get(f"{API_URI}/discover/movie?api_key={API_KEY}&primary_release_year={year}&page={page}").json()

                    for jmovie in movies['results']:
                        current_id = jmovie.get('id')
                        jmovie = rq.get(f"{API_URI}/movie/{jmovie.get('id')}?api_key={API_KEY}").json()
                        movie, _ = Movie.objects.get_or_create(
                            id = jmovie.get('id'),
                            poster = jmovie.get('poster_path', '') if jmovie.get('poster_path') is not None else '',
                            adult = jmovie.get('adult', False),
                            overview = jmovie.get('overview') if jmovie.get('overview') is not None else '',
                            release_date = jmovie.get('release_date', ''),
                            original_title = jmovie.get('original_title', ''),
                            original_language = jmovie.get('original_language', ''),
                            title = jmovie.get('title', ''),
                            popularity = jmovie.get('popularity', 0),
                            vote_count = jmovie.get('vote_count', 0),
                            vote_average = jmovie.get('vote_average', 0),
                            imdb_id = jmovie.get('imdb_id') if jmovie.get('imdb_id') is not None else '',
                            budget = jmovie.get('budget', 0),
                            revenue = jmovie.get('revenue', 0),
                            runtime = jmovie.get('runtime') if jmovie.get('runtime') is not None else 0,
                            status = jmovie.get('status', ''),
                            tagline = jmovie.get('tagline') if jmovie.get('tagline') is not None else '',
                        )

                        for jgenre in jmovie.get('genre_ids', []):
                            movie.genres.add(jgenre)

                        for prod_count in jmovie.get('production_countries', []):
                            obj, _ = Production_Country.objects.get_or_create(
                                iso = prod_count.get('iso_3166_1'),
                                name = prod_count.get('name', '')
                            )
                            movie.production_countries.add(obj)

                        for prod_comp in jmovie.get('production_companies', []):
                            obj, _ = Production_Company.objects.get_or_create(
                                id = prod_comp.get('id'),
                                logo = prod_comp.get('logo_path') if prod_comp.get('logo_path') is not None else "",
                                name = prod_comp.get('name', ''),
                                origin_country = prod_comp.get('origin_country', '')
                            )
                            movie.production_companies.add(obj)

                        for lang in jmovie.get('spoken_languages', []):
                            obj, _ = Spoken_Languages.objects.get_or_create(
                                iso = lang.get('iso_639_1'),
                                name = lang.get('name')
                            )
                            movie.spoken_languages.add(obj)
                        
                        movie.save()
        except Exception as e:
            print(e)
            print(current_id)
