def cal_c():
    from scipy.stats import mvn
    import numpy as np
    low = np.array([0, 0])
    upp = np.array([1, 1])
    mu = np.array([.5, .5])
    S = np.array([[1, 0],[0, 1]])
    p, i = mvn.mvnun(low, upp, mu, S)
    print(p, i)

    low = np.array([0, 0])
    upp = np.array([1, 1])
    mu = np.array([.5, .5])
    S = np.array([[.1, 0], [0, 0.1]])
    p, i = mvn.mvnun(low, upp, mu, S)
    print(p, i)

    low = np.array([-.5, -.5])
    upp = np.array([.5, .5])
    mu = np.array([0, 0])
    S = np.array([[1, 0], [0, 1]])
    p, i = mvn.mvnun(low, upp, mu, S)
    print(p, i)

    return p

cal_c()