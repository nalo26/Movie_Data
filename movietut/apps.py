from django.apps import AppConfig
from threading import Thread



class MovietutConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movietut'
    
    def ready(self):
        from .refresh_movies import background_refresh_movie
        from .clusterImpl import init
        refreshMovieThread = Thread(target=background_refresh_movie, args=(10,))
        refreshMovieThread.start()
        createClusterThread = Thread(target=init)
        createClusterThread.start()        