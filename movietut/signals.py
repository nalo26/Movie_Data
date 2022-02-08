from threading import Thread
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from movietut.models import Cluster

@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    # processRecommendedThread = Thread(target=processRecommendedMovies, args=(user,), daemon=True)
    # processRecommendedThread.start()
    processRecommendedMovies(user)
    
def processRecommendedMovies(user):
    user.recommended.clear()
    likedMovies = [movie for movie in user.movies.all() if movie.isLiked]

    allClusters = Cluster.objects.all()
    clusters = {cluster: 0 for cluster in allClusters}

    for c in allClusters:
        for movie in c.movies.all(): 
            if movie in likedMovies: clusters[c] += 1

    cluster = max(clusters, key=clusters.get)

    memberGenres = user.genres.all()

    for movie in cluster.movies.all():
        if len(memberGenres) == 0 or any(g in memberGenres for g in movie.genres.all()):
            user.recommended.add(movie)
        
    user.save()