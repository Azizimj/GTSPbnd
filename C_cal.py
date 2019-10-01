import csv
from scipy.integrate import dblquad
import math
import time

def cal_c():
    from scipy.stats import mvn
    import numpy as np
    low = np.array([0, 0])
    upp = np.array([1, 1])
    mu = np.array([.5, .5])
    sigx = 1
    S = np.array([[sigx, 0], [0, sigx]])
    scale = 1
    p, i = mvn.mvnun(low, upp, mu, S)
    # print(p, i)
    return p*scale

def write_on_csv(n,k,m,res,t):

    row = [n,k,m,res,t]

    with open('result_integ.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()
    return

def integ_trun(n,k):

    t_ = time.time()
    # n = 15
    # k = 3
    m =1
    mux = 0.5
    muy = 0.5
    c = 2* cal_c()
    epsrel_ = 1e-4
    epsabs_ = 1.49e-8
    sigx = 1

    area = dblquad(lambda x, y:math.sqrt(k/(c*math.pi)**k*math.exp(-(x-mux)**2/(2*sigx)-(y-muy)**2/(2*sigx))*(dblquad(lambda x1,y1:math.exp(-(x1-mux)**2/(2*sigx)-(y1-muy)**2/(2*sigx))*int((x1-mux)**2/sigx+(y1-muy)**2/sigx<(x-mux)**2/sigx+(y-muy)**2/sigx),0,1,0,1,epsabs=epsabs_, epsrel=epsrel_))[0]**(k-1))
                   , 0, 1, 0, 1, epsrel =epsrel_, epsabs=epsabs_)
    print(area)
    res = n ** (1 / 2) * area[0]
    print("n {}, k {}, m {}, res {} ".format(n,k,m,res))
    print(time.time()-t_)
    write_on_csv(n,k,m,res,time.time()-t_)

    return res

if __name__ == '__main__':
    import time, sys

    t_ = time.time()
    if len(sys.argv)>1:
        n = int(sys.argv[1])
        k = int(sys.argv[2])
        # m = int(sys.argv[2])
        integ_trun(n,k)

    import multiprocessing as mp
    from itertools import product

    pool = mp.Pool(mp.cpu_count())
    par = {}
    par['low_n'] = 30
    par['up_n'] = 50
    par['step_n'] = 5

    par['low_k'] = 3
    par['up_k'] = 8
    par['step_k'] = 3

    par['low_m'] = 1
    par['up_m'] = 1
    par['step_m'] = 1

    par['seed_l'] = 100
    par['seed_u'] = 105
    par['seed_step'] = 1

    # pool async parall
    results = []
    def collect_result(result):
        global results
        results.append(result)


    for n, k in product(range(par['low_n'], par['up_n'] + 1, par['step_n']),
                                  range(par['low_k'], par['up_k'] + 1, par['step_k'])):
        pool.apply_async(integ_trun, args=(n, k), callback=collect_result)
    pool.close()
    pool.join()
    results.sort(key=lambda x: x[0])
    results_final = [r for i, r in results]
    print(results_final)

    # pool apply parall
    # results = [pool.apply(integ_trun, args=(n, k)) for n, k in product(range(low_n, up_n + 1), range(low_k, up_k + 1))]
    # pool.close()
    # print(results)

    print("total time: {}".format(time.time()-t_) )