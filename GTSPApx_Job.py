import os
import time
import sys

def make_dir(dir):
    if not os.path.exists(dir):
        print("dir ( {} ) is made ".format(dir))
        os.mkdir(dir)

hpc_is = False

# num_clusters_card_m = [(5,2,1,'GTSP'),(5,2,1,'MST'),(5,2,1,'NN'),
#                        (5,4,2,'GTSP'),(5,4,2,'MST'),(5,4,2,'NN'),
#                        (10,2,1,'GTSP'),(10,2,1,'MST'),(10,2,1,'NN'),
#                        (10,4,2,'GTSP'),(10,4,2,'MST'),(10,4,2,'NN'),
#                        (20,5,1,'GTSP'),(20,5,1,'MST'),(20,5,1,'NN')]

# num_clusters_card_m = [(4,3,1),(5,2,1),(5,2,2),(6,2,1),(5,3,1),(10,2,1),(20,4,2)]
# num_clusters_card_m = [(4,4,1), (4,5,2), (5,5,1), (5,5,2), (3,5,1)]
# num_clusters_card_m = [(4,5,1), (5,4,2), (5,5,2), (3,8,2), (3,8,1), (6,4,1)]
num_clusters_card_m = [(3,5,2), (3,6,1), (5,3,1), (3,8,1)]
# ,(6,2,1),(5,4,2),(10,3,1),(11,3,1),(12,3,1)
# seeds = [111,222,333,444,555,666,777,888,999,1111,2222,3333,4444,5555,6666,7777,8888,9999,1010,2020]
seeds = [555,666,777,888,999,113]

if hpc_is:

    time_ = '24:00:00'
    jobs_files = []
    hdir = "/auto/rcf-proj2/ma2/azizim/GTSP"
    pdir = "/usr/usc/python/3.6.0/setup.sh"
    julia_dir = "/usr/usc/julia/1.1.1/setup.sh"
    gurobi_dir_ = "/usr/usc/gurobi/default/setup.sh"


    for seed_g in seeds:
        for num_cluster, card, m in num_clusters_card_m:
            ntasks = min(30 * num_cluster * card, 1000)
            mem_per_cpu = "8G"
            # jname = model_+"_"+ str(num_cluster)+"_"+str(card)+"_"+str(m)
            jname = str(num_cluster) + "_" + str(card) + "_" + str(m) +"_" + str(seed_g)
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
            f.write("source " + gurobi_dir_ + "\n")
            f.write("julia Adcut.jl " + str(num_cluster) + " "
                    + str(card) + " " + str(m) +" " + str(seed_g) + " > " + jname + ".txt \n")
            print(jname)
            f.close()

    time.sleep(2)

    make_dir("log_")
    f_jobs = open("log_/jobs.txt","a")
    f_jobs.write("#############################\n")

    for jname in jobs_files:
        os.system("sbatch "+jname)
        f_jobs.write(jname+"\n")
        time.sleep(2)
    f_jobs.close()

else:
    make_dir("log_")
    f_jobs = open("log_/jobs.txt", "a")
    f_jobs.write("#############################\n")

    for seed_g in seeds:
        for num_cluster, card, m in num_clusters_card_m:
            jname = str(num_cluster) + "_" + str(card) + "_" + str(m) + "_" + str(seed_g)
            f_jobs.write(jname + "\n")
            print("job {} started".format(jname))
            st_t = time.time()
            os.system("julia Adcut.jl " + str(num_cluster) + " "
                     + str(card) + " " + str(m) + " " + str(seed_g) + " > " + jname + ".txt \n")
            print("job {} end in {} sec".format(jname, time.time()-st_t))
            time.sleep(1)