from sklearn.cluster import KMeans
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
cur.execute("select m.vote_average, m.popularity from movietut_movie m join movietut_movie_production_countries mpc on m.id = mpc.movie_id where m.popularity < 80 and m.vote_average > 0 ")#and mpc.production_country_id in ('FR', 'US')")
results = cur.fetchall();

conn.close()
allMoviesMatrix = np.array(results)

# Generate sample data
n_components = 500
'''
n_samples = 400000

X, y_true = make_blobs(n_samples=n_samples,
                       centers=n_components,
                       cluster_std=0.60,
                       random_state=4)
X = X[:, ::-1]
'''
# Calculate seeds from kmeans++
model = KMeans(n_clusters=n_components, init='k-means++')
yhat = model.fit_predict(allMoviesMatrix)
centers_init = model.cluster_centers_
# Plot init seeds along side sample data
plt.figure(1)
colors = randomColors(n_components)

for k, col in enumerate(colors):
    cluster_data = yhat == k
    plt.scatter(allMoviesMatrix[cluster_data, 0], allMoviesMatrix[cluster_data, 1],
                c=col, marker='.', s=20)

plt.xlim(0,10)
plt.ylim(0,80)
plt.scatter(centers_init[:, 0], centers_init[:, 1], c='b', s=30)
plt.title("Kek-Means+- CovInitialization")
plt.xticks([])
plt.yticks([])
plt.show()

