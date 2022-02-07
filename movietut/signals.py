from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from movietut.models import Cluster

@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):

    likedMovies = [movie for movie in user.movies if movie.isLiked]

    allClusters = Cluster.objects.all()
    clusters = {cluster: 0 for cluster in allClusters}

    for c in allClusters:
        for movie in c: 
            if movie in likedMovies: clusters[c] += 1

    cluster = max(clusters, key=clusters.get)

    recommendedMovies = list()
    memberGenres = user.genres

    for movie in cluster.movies:
        if movie.genre in memberGenres: recommendedMovies.append(movie)
    
    user.recommended = recommendedMovies