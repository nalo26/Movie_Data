from django.db import models
from sklearn.cluster import KMeans
from movietut.models import Movie
from django.db.models import Q
import numpy as np
import matplotlib.pyplot as plt
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
    n_components = 500 # TODO: put it back to 500
    matrix, yhat, centers_init = create_cluster(n_components)
    # Plot init seeds along side sample data
    # plt.figure(1)
    colors = randomColors(n_components)
    # print(matrix)

    pop = dict()

    for k, col in enumerate(colors):
        cluster_data = yhat == k
    #     plt.scatter(matrix[cluster_data, 0], matrix[cluster_data, 1],
    #                 c=col, marker='.', s=20)

        pop[k] = list()
        for index in range(len(cluster_data)):
            if cluster_data[index]:
                pop[k].append(matrix[index, 1])

    # plt.xlim(0,10)
    # plt.ylim(0,10)
    # plt.scatter(centers_init[:, 0], centers_init[:, 1], c='b', s=30)
    # plt.title("Kek-Means+- CovInitialization")
    # plt.xticks([])
    # plt.yticks([])
    # plt.show()

    searchPop(125, pop)

def searchPop(cluster, pop):
    pop = pop[cluster]
    movies = list()

    for movie in pop:
        qset = Movie.objects.all().filter(Q(production_countries="FR") | Q(production_countries="US"), popularity=movie).values_list("id")
        # print(qset)
        for m in qset:
            movies.append(m[0])

    # print(movies)
    with open('recommended_movies.json', 'w') as f:
        json.dump(movies, f)

    print(f"YHATED {len(movies)} movies")