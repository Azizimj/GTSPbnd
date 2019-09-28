from scipy.stats import mvn
import numpy as np

low = np.array([0, 0])
upp = np.array([1, 1])
mu = np.array([.5, .5])
S = np.array([[0.1, 0],[0.1, 0]])
p, i = mvn.mvnun(low,upp,mu,S)
print(.2*p, i)