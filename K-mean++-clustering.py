import pickle
import numpy as np

def eucl_dist(a, b, axis=1):
    return np.linalg.norm(a - b, axis=axis)

def get_center(k, X):
    temp = []
    temp.append(X[np.random.randint(0, len(X))])
    while len(temp)<k:
        d2 = np.array([min([np.square(eucl_dist(i,c, None)) for c in temp]) for i in X])
        prob = d2/d2.sum()
        cum_prob = prob.cumsum()
        r = np.random.random()
        ind = np.where(cum_prob >= r)[0][0]
        temp.append(X[ind])
    return np.array(temp)

def k_mean_pp(x, k):
    # error = {key:0.0 for key in range(2,11)}

    # initalizing cluster variable
    center = get_center(k, x)

    # for k in range(2,11):

    # assigining zeros to old centroids value
    center_old = np.zeros(center.shape)

    # initial error
    err = eucl_dist(center, center_old, None)

    while err != 0:

        # calculatin distance of data points from centroids and assiging min distance cluster centroid as data point cluster
        for i in range(len(x)):
            distances = eucl_dist(x[i], center)
            clust = np.argmin(distances)
            cluster[i] = clust

        # changing old centroids value
        center_old = np.copy(center)

        # Finding the new centroids by taking the average value
        for i in range(k):
            points = [x[j] for j in range(len(x)) if cluster[j] == i]
            if points:
                center[i] = np.mean(points, axis=0)

        # calculation difference between new centroid and old centroid values
        err = eucl_dist(center, center_old, None)

    # calculation total difference between cluster centroids and cluster data points
    error = 0
    for i in range(k):
        d = [eucl_dist(x[j], center[i], None) for j in range(len(x)) if cluster[j] == i]
        error += np.sum(d)

    # counting data points in all clusters
    count = {key: 0.0 for key in range(k)}
    for i in range(len(x)):
        count[cluster[i]] += 1

    # displaying cluster number, average distance between centroids and data points and cluster count
    print k, error / len(x), count

    return cluster

if __name__ == '__main__':

    # loading dataset of form [[data1],[data2], ....]
    # inp = pickle.load(open('/media/zero/41FF48D81730BD9B/all-the-news/4/temp_tokenize_dec_dataset/test.pickle', 'rb'))
    x = np.array([i[0] for i in inp])

    # return cluster number for every data
    cluster = k_mean_pp(x)
