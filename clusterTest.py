from sklearn.cluster import kmeans_plusplus
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import psycopg2
import numpy as np
import random

def randomColors(numbers):
    return ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for _ in range(numbers)] 

conn = psycopg2.connect(
    host="localhost",
    database="movie_db",
    user="movie",
    password="movie")

cur = conn.cursor();
cur.execute("select m.vote_average, m.popularity from movietut_movie m join movietut_movie_production_countries mpc on m.id = mpc.movie_id where m.popularity < 80 and m.vote_average > 0 and mpc.production_country_id in ('FR', 'US')")
results = cur.fetchall();

conn.close()
allMoviesMatrix = np.array(results)

# Generate sample data
n_components = 20
'''
n_samples = 400000

X, y_true = make_blobs(n_samples=n_samples,
                       centers=n_components,
                       cluster_std=0.60,
                       random_state=4)
X = X[:, ::-1]
'''
# Calculate seeds from kmeans++
centers_init, _ = kmeans_plusplus(allMoviesMatrix, n_clusters=n_components,
                                        random_state=0)
model = KMeans(n_clusters=10)
yhat = model.fit_predict(allMoviesMatrix)
# Plot init seeds along side sample data
plt.figure(1)
colors = randomColors(n_components)

for k, col in enumerate(colors):
    cluster_data = yhat == k
    plt.scatter(allMoviesMatrix[cluster_data, 0], allMoviesMatrix[cluster_data, 1],
                c=col, marker='.', s=10)

plt.scatter(centers_init[:, 0], centers_init[:, 1], c='b', s=50)
plt.title("Kek-Means+- CovInitialization")
plt.xticks([])
plt.yticks([])
plt.show()

