import os
import time
import sys

def make_dir(dir):
    if not os.path.exists(dir):
        print("dir ( {} ) is made ".format(dir))
        os.mkdir(dir)

hpc_is = True

if hpc_is:

    time_ = '24:00:00'
    jobs_files = []
    hdir = "/auto/rcf-proj2/ma2/azizim/ApxGTSP"
    pdir = "/usr/usc/python/3.6.0/setup.sh"
    julia_dir = "/usr/usc/julia/1.1.1/setup.sh"
    # gurobi_dir_ = "/usr/usc/gurobi/default/setup.sh"

    ins_folder = "GLNSLIB_RANDOM_TPP/"
    ins_prefix = "TPP_input_"

    low_n = 30
    up_n = 35
    step_n = 10
    low_k = 3
    up_k = 3
    step_k = 1
    low_m = 1
    up_m = 1
    step_m = 1
    seed_l = 100
    seed_u = 100
    seed_step = 1

    from itertools import product
    for n, k, m, seed_ in product(range(low_n, up_n + 1, step_n), range(low_k, up_k + 1, step_k),
                           range(low_m, up_m + 1, step_m),range(seed_l, seed_u + 1, seed_step)):
        if k >= m:
            ntasks = min(10 * n * k, 1000)
            mem_per_cpu = "4G"
            jname = str(n) + "_" + str(k) + "_" + str(m) + "_" + str(seed_)
            f = open(jname + ".slurm", "w")
            jobs_files.append(jname + ".slurm")
            f.write("#!/bin/bash \n")
            f.write("#SBATCH --ntasks={}\n".format(ntasks))
            f.write("#SBATCH --mem-per-cpu={}\n".format(mem_per_cpu))
            f.write("#SBATCH --time={}\n".format(time_))
            f.write("#SBATCH --output=O" + jname + ".txt" + "\n")
            f.write("#SBATCH --error=" + "e" + jname + ".txt" + "\n")
            f.write("#SBATCH --job-name=" + jname + "\n")
            f.write("cd " + hdir + "\n")
            f.write("source " + julia_dir + "\n")
            f.write("source " + pdir + "\n")
            # f.write("source " + gurobi_dir_ + "\n")
            f.write("python generate_random_TPP_tests.py " + str(n) + " " + str(k) + " " + str(m) + " " + str(seed_) + "\n")
            f.write("julia GLNS_Sim.jl "+ ins_folder + " " + ins_prefix + jname + ".gtsp > " + jname + ".txt \n")
            print(jname)
            f.close()

    time.sleep(2)

    make_dir("log_")
    f_jobs = open("log_/jobs.txt","a")
    f_jobs.write("#############################\n")

    # for jname in jobs_files:
    #     os.system("sbatch "+jname)
    #     f_jobs.write(jname+"\n")
    #     time.sleep(2)
    # f_jobs.close()