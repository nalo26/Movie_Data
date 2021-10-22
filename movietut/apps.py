from django.apps import AppConfig
from threading import Thread


class MovietutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movietut'
    
    def ready(self):
        from .refresh_movies import background_refresh_movie
        t = Thread(target=background_refresh_movie, args=(10,))
        t.start()        