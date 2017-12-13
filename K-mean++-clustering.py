import pickle
import numpy as np

def eucl_dist(a, b, axis=1):
    return np.linalg.norm(a - b, axis=axis)

context=4
inp = pickle.load(open('/home/zero/Downloads/all-the-news/'+str(context)+'/temp_tokenize_dec_dataset/1.pickle','rb'))
x = np.array([i[0][context-1:context+1] for i in inp])

cluster = np.zeros(x.shape[0])

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


# error = {key:0.0 for key in range(2,11)}

for l in range(5):
    k=5
    error = 0
    center = get_center(k, x)

    center_old = np.zeros(center.shape)
    err = eucl_dist(center, center_old, None)

    while err != 0:
        for i in range(len(x)):
            distances = eucl_dist(x[i], center)
            clust = np.argmin(distances)
            cluster[i] = clust

        center_old = np.copy(center)

        # Finding the new centroids by taking the average value
        for i in range(k):
            points = [x[j] for j in range(len(x)) if cluster[j] == i]
            if points:
                center[i] = np.mean(points, axis=0)
        err = eucl_dist(center, center_old, None)
        # print err

    for i in range(k):
        d = [eucl_dist(x[j],center[i],None) for j in range(len(x)) if cluster[j] == i]
        error += np.sum(d)

    count = {key: 0.0 for key in range(k)}
    for i in range(len(x)):
        count[cluster[i]] += 1
    print k, error, count

