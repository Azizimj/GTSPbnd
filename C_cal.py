
def cal_c():
    from scipy.stats import mvn
    import numpy as np


    low = np.array([0, 0])
    upp = np.array([1, 1])
    mu = np.array([.5, .5])
    S = np.array([[0.1, 0],[0.1, 0]])
    p, i = mvn.mvnun(low,upp,mu,S)
    # print(.2*p, i)
    return p

def integ_trun():
    from scipy.integrate import dblquad
    import math
    n = 5
    k = 2
    m =1
    mux = 0.5
    muy = 0.5
    c = 2* cal_c()
    epsrel_ = 1e-4
    epsabs_ = 1.49e-8

    area = dblquad(lambda x, y:math.sqrt(k/(c*math.pi)**k*math.exp(-(x-mux)**2/0.2-(y-muy)**2/0.2)*(dblquad(lambda x1,y1:math.exp(-(x1-mux)**2/0.2-(y1-muy)**2/0.2)*int((x1-mux)**2/0.2+(y1-muy)**2/0.2<(x-mux)**2/0.2+(y-muy)**2/0.2),0,1,0,1,epsabs=epsabs_, epsrel=epsrel_))[0]**(k-1))
                   , 0, 1, 0, 1,epsrel =epsrel_,epsabs=epsabs_)
    print(area)
    print(n**(1/2)*area)

if __name__ == '__main__':
    import time
    t_ = time.time()
    integ_trun()
    print("time: {}".format(time.time()-t_) )