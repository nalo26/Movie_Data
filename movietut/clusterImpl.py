import os
from sklearn.cluster import KMeans
from movietut.models import Movie
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
    if os.path.exists("recommended_movies.json"):
        os.remove("recommended_movies.json")
        
    n_components = 50
    matrix, yhat, centers_init = create_cluster(n_components)

    pop = dict()

    for k in range(n_components):
        cluster_data = yhat == k

        pop[k] = list()
        for index in range(len(cluster_data)):
            if cluster_data[index]:
                pop[k].append(matrix[index, 1])

    searchPop(12, pop)

def searchPop(cluster, pop):
    pop = pop[cluster]
    movies = list()

    for movie in pop:
        qset = Movie.objects.all().filter(Q(production_countries="FR") | Q(production_countries="US"), popularity=movie).values_list("id")
        for m in qset:
            movies.append(m[0])

    with open('recommended_movies.json', 'w') as f:
        json.dump(movies, f)

    print(f"Loaded {len(movies)} movies recommendation")