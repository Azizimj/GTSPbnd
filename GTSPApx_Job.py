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

    par = {}
    par['low_n'] = 30
    par['up_n'] = 50
    par['step_n'] = 5

    par['low_k'] = 3
    par['up_k'] = 8
    par['step_k'] = 3

    par['low_m']= 1
    par['up_m'] = 1
    par['step_m'] = 1

    par['seed_l'] = 100
    par['seed_u'] = 105
    par['seed_step'] = 1

    from itertools import product
    for n, k, m, seed_ in product(range(par['low_n'], par['up_n'] + 1, par['step_n']), range(par['low_k'], par['up_k'] + 1, par['step_k']),
                           range(par['low_m'], par['up_m'] + 1, par['step_m']),range(par['seed_l'], par['seed_u'] + 1, par['seed_step'])):
        if k >= m:
            ntasks = min(n * k, 1000)
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
            f.write("python3 generate_random_TPP_tests.py " + str(n) + " " + str(k) + " " + str(m) + " " + str(seed_) + "\n")
            f.write("julia GLNS_Sim.jl "+ ins_folder + " " + ins_prefix + jname + ".gtsp > " + jname + ".txt \n")
            print(jname)
            f.close()

    time.sleep(2)

    make_dir("log_")
    f_jobs = open("log_/jobs.txt","a")
    f_jobs.write("#############################\n")
    f_jobs.write(str(par))
    f_jobs.write("\n")

    for jname in jobs_files:
        os.system("sbatch "+jname)
        f_jobs.write(jname+"\n")
        time.sleep(1)
    f_jobs.close()