from django.core.management import BaseCommand
import requests as rq
from movietut.models import Movie, Production_Country, Production_Company, Spoken_Languages
import asyncio

# async def bg_loop():
def bg_loop():
    API_URI = "https://api.themoviedb.org/3/movie/latest"
    API_KEY = "e7e2852e5b4d9cc2fccd5fb9858411d9"

    latest_inserted = None        
    # while True:
    jmovie = rq.get(f"{API_URI}?api_key={API_KEY}").json()

    # if not(latest_inserted == None or jmovie.get('id', None) != latest_inserted): continue

    latest_inserted = jmovie.get('id')

    movie, _ = Movie.objects.update_or_create(
        id = jmovie.get('id'),
        defaults = {
            "poster": jmovie.get('poster_path', '') if jmovie.get('poster_path') is not None else '',
            "adult": jmovie.get('adult', False),
            "overview": jmovie.get('overview') if jmovie.get('overview') is not None else '',
            "release_date": jmovie.get('release_date', ''),
            "original_title": jmovie.get('original_title', '')[:200],
            "original_language": jmovie.get('original_language', ''),
            "title": jmovie.get('title', '')[:200],
            "popularity": jmovie.get('popularity', 0),
            "vote_count": jmovie.get('vote_count', 0),
            "vote_average": jmovie.get('vote_average', 0),
            "imdb_id": jmovie.get('imdb_id') if jmovie.get('imdb_id') is not None else '',
            "budget": jmovie.get('budget', 0),
            "revenue": jmovie.get('revenue', 0),
            "runtime": jmovie.get('runtime') if jmovie.get('runtime') is not None else 0,
            "status": jmovie.get('status', ''),
            "tagline": jmovie.get('tagline') if jmovie.get('tagline') is not None else '',
        }
    )

    for jgenre in jmovie.get('genres', []):
        movie.genres.add(jgenre.get('id'))

    for prod_count in jmovie.get('production_countries', []):
        obj, _ = Production_Country.objects.get_or_create(
            iso = prod_count.get('iso_3166_1'),
            name = prod_count.get('name', '')
        )
        movie.production_countries.add(obj)

    for prod_comp in jmovie.get('production_companies', []):
        obj, _ = Production_Company.objects.update_or_create(
            id = prod_comp.get('id'),
            defaults = {
                "logo": prod_comp.get('logo_path') if prod_comp.get('logo_path') is not None else "",
                "name": prod_comp.get('name', ''),
                "origin_country": prod_comp.get('origin_country') if prod_comp.get('origin_country') is not None else ""
            }
        )
        movie.production_companies.add(obj)

    for lang in jmovie.get('spoken_languages', []):
        obj, _ = Spoken_Languages.objects.get_or_create(
            iso = lang.get('iso_639_1'),
            name = lang.get('name')
        )
        movie.spoken_languages.add(obj)

    movie.save()
    print(f"[+] {movie.title}")
    # await asyncio.sleep(10)


class Command(BaseCommand):
    def handle(self, *args, **options):
        bg_loop()