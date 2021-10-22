from django.db import models
from sklearn.cluster import KMeans
from movietut.models import Movie
from django.db.models import Q
import numpy as np
import matplotlib.pyplot as plt
import random

def randomColors(numbers):
    return ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for _ in range(numbers)] 

def create_cluster(nbCluster):
    model = KMeans(n_clusters=nbCluster, init='k-means++')
    movieMatrix = np.array(Movie.objects.all().values_list("vote_average", "popularity")
    .filter(Q(production_countries="FR") | Q(production_countries="US")))
    yhat = model.fit_predict(movieMatrix)
    return movieMatrix, yhat, model.cluster_centers_


def init():
    n_components = 500
    matrix, yhat, centers_init = create_cluster(n_components)
    # Plot init seeds along side sample data
    plt.figure(1)
    colors = randomColors(n_components)

    for k, col in enumerate(colors):
        cluster_data = yhat == k
        plt.scatter(matrix[cluster_data, 0], matrix[cluster_data, 1],
                    c=col, marker='.', s=20)
    plt.xlim(0,10)
    plt.ylim(0,10)
    plt.scatter(centers_init[:, 0], centers_init[:, 1], c='b', s=30)
    plt.title("Kek-Means+- CovInitialization")
    plt.xticks([])
    plt.yticks([])
    plt.show()




