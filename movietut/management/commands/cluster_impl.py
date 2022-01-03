from django.core.management import BaseCommand
import movietut.clusterImpl as cl
import random
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def randomColors(numbers):
    return ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for _ in range(numbers)] 

class Command(BaseCommand):
    def handle(self, *args, **options):
            n_components = 500
            matrix, yhat, centers_init = cl.create_cluster(n_components)
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