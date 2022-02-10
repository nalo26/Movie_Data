from django.apps import AppConfig
from threading import Thread
import os


class MovietutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movietut'
    
    def ready(self):
        import movietut.signals
        if os.environ.get('RUN_MAIN', None) != 'true':
            from .refresh_movies import background_refresh_movie
            from .clusterImpl import init
            refreshMovieThread = Thread(target=background_refresh_movie, args=(86400,), daemon=True)
            refreshMovieThread.start()
            createClusterThread = Thread(target=init, daemon=True)
            createClusterThread.start()   
