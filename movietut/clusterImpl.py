import os
from sklearn.cluster import KMeans
from movietut.models import Cluster, Movie
from django.db import transaction
from django.db.models import Q
import numpy as np
import random
import json


def randomColors(numbers):
    return ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for _ in range(numbers)] 

def create_cluster(nbCluster):
    model = KMeans(n_clusters=nbCluster, init='k-means++')
    movieMatrix = np.array(Movie.objects.all().values_list("vote_average", "popularity")
    .filter(Q(production_countries="FR") | Q(production_countries="US")))
    yhat = model.fit_predict(movieMatrix)
    return movieMatrix, yhat, model.cluster_centers_


def init():
        
    n_components = 50
    matrix, yhat, centers_init = create_cluster(n_components)

    pop = dict()

    with transaction.atomic():
        for k in range(n_components):
            print(k)
            cluster_data = yhat == k

            pop[k] = list()
            for index in range(len(cluster_data)):
                if cluster_data[index]:
                    pop[k].append(matrix[index, 1])

            if k == 0: continue

            cluster = Cluster()
            cluster.save()
            movies_to_add = searchPop(pop[k])
            for movie in movies_to_add:
                cluster.movies.add(movie)
            cluster.save()
    
    print("done")

def searchPop(pop):
    movies = set()

    for movie in pop[:50]:
        qset = Movie.objects.all().filter(Q(production_countries="FR") | Q(production_countries="US"), popularity=movie).values_list("id")
        for m in qset:
            movies.add(m[0])

    return movies
    


