#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 23:28:27 2019

@author: jiachuan_chen
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This file is to generate the small random GTSP tests to compare the performance between WTSP and GLNS
Created on Tue Mar 19 21:12:30 2019

@author: jiachuan_chen
"""

import numpy as np
import os
import time
import random
import math
import sys
# global constant
# for GLNS proof test, set M to be 0
M = 0
infty = 10000

def make_dir(dir):
    if not os.path.exists(dir):
        print("dir ( {} ) is made ".format(dir))
        os.mkdir(dir)

def write_WTSP_instance(distance_matrix, clusters, visit_times, input_file_name):
    dir_ = "WTSPLIB_RANDOM_TPP/"
    make_dir(dir_)
    # os.chdir(dir_)
    f = open(dir_+input_file_name + ".gtsp", "w")
    f.write("NAME :" + input_file_name + "\n")
    f.write("NUM_VERTICES\n")
    f.write(str(len(distance_matrix)) + "\n")
    f.write("NUM_CLUSTERS\n")
    f.write(str(len(clusters)) + "\n")
    f.write("Full Matrix\n")
    for i in range(len(distance_matrix)):
        for j in range(len(distance_matrix)):
            f.write(" " + str(float(distance_matrix[i, j])))
        f.write("\n")
    f.write("GTSP_SET_SECTION\n")
    for i in range(len(clusters)):
        for j in range(len(clusters[i])):
            f.write(str(clusters[i][j]) + " ")
        f.write("\n")
    f.write("GTSP_Visit_SECTION\n")
    for i in range(len(visit_times)):
        f.write(str(visit_times[i]))
        f.write("\n")
    f.write("EOF")
    f.close()
    return

    
def write_tpp_file_to_glns(distance_matrix, cluster, input_file_name):
    # must use a different matrix
    distance_matrix_glns = distance_matrix * 1000 # scale here is 1000
    distance_matrix_glns = distance_matrix_glns.round()
    dir_ = "GLNSLIB_RANDOM_TPP/"
    make_dir(dir_)
    # os.chdir(dir_)
    f = open(dir_+input_file_name + ".gtsp", "w")
    f.write("NAME : " + input_file_name + "\n")
    f.write("TYPE : GTSP\n")
    f.write("DIMENSION : " + str(len(distance_matrix_glns)) + "\n")
    f.write("GTSP_SETS : " + str(len(cluster)) + "\n")
    f.write("EDGE_WEIGHT_TYPE : EXPLICIT\n")
    f.write("EDGE_WEIGHT_FORMAT : FULL_MATRIX \n")
    f.write("EDGE_WEIGHT_SECTION\n")
    for i in range(len(distance_matrix_glns)):
        for j in range(len(distance_matrix_glns)):
            f.write(" " + str(int(distance_matrix_glns[i, j])))
        f.write("\n")
    f.write("GTSP_SET_SECTION\n")
    for i in range(len(cluster)):
        f.write(str(i + 1) + " ")
        for j in range(len(cluster[i])):
            f.write(str(cluster[i][j]) + " ")
        f.write(str(-1) + "\n")
    f.write("EOF\n")
    f.close()
    return

## The input clusters starts from index 0
def trans_to_GTSP(distance_matrix, clusters, visit_times):
    num_visit_vertices = distance_matrix.shape[0]
    crt_vertex = num_visit_vertices
    #to_not_visit = []
    #to_not_visit.append(0)
    not_visit_vertex_list = []
    ret_clusters = []
    ret_clusters.append([0])
    for i in range(1, num_visit_vertices):
        #to_not_visit.append(crt_vertex)
        not_visit_vertex_list.append(crt_vertex)
        ret_clusters.append([i, crt_vertex])
        crt_vertex += 1
    dummy_lists = []
    for i in range(1, len(clusters)):
        cluster = clusters[i]
        visit_time = visit_times[i]
        dummy_len = len(cluster) - visit_time
        dummy_list = []
        for j in range(dummy_len):
            dummy_list.append(crt_vertex)
            ret_clusters.append([crt_vertex])
            crt_vertex += 1
        dummy_lists.append(dummy_list)
    ret_matrix = np.ones((crt_vertex, crt_vertex)) * infty
    assert len(clusters) == len(dummy_lists) + 1
    for i in range(1, len(clusters)):
        for j in clusters[i]:
            for k in dummy_lists[i - 1]:
                ret_matrix[j + num_visit_vertices - 1, k] = M
    for i in range(2 * num_visit_vertices - 1, crt_vertex):
        for j in not_visit_vertex_list:
            ret_matrix[i, j] = M
    for i in range(num_visit_vertices):
        for j in range(num_visit_vertices):
            ret_matrix[i, j] = distance_matrix[i, j]
    for i in range(num_visit_vertices):
        for j in not_visit_vertex_list:
            if j - i == num_visit_vertices - 1:
                continue
            ret_matrix[i, j] = distance_matrix[i, 0]
    for i in range(2 * num_visit_vertices - 1, crt_vertex):
        ret_matrix[i, 0] = M
    for ret_cluster in ret_clusters:
        for i in range(len(ret_cluster)):
            ret_cluster[i] += 1
    return [ret_matrix, ret_clusters]


def gen_rand_TPP(num_clusters, min_card, max_card, x_limit, y_limit, visit_time):
    data_points = []
    clusters = []
    crt_vertex = 0
    visit_times = []
    for i in range(num_clusters):
        if i == 0:
            temp_x = random.uniform(0, x_limit)
            temp_y = random.uniform(0, y_limit)
            data_points.append([temp_x, temp_y])
            clusters.append([crt_vertex])
            visit_times.append(1)
            crt_vertex += 1
        else:
            temp_k = random.randint(min_k, max_k)
            temp_cluster = []
            for j in range(temp_k):
                temp_x = random.uniform(0, x_limit)
                temp_y = random.uniform(0, y_limit)
                data_points.append([temp_x, temp_y])
                temp_cluster.append(crt_vertex)
                crt_vertex += 1
            clusters.append(temp_cluster)
            visit_times.append(visit_time)
    distance_matrix = np.ones((len(data_points), len(data_points))) * infty
    for i in range(len(data_points)):
        for j in range(len(data_points)):
            if i != j:
                distance_matrix[i, j] = get_distance(data_points[i], data_points[j])
    return [distance_matrix, clusters, visit_times, data_points]


def get_distance(a, b):
    x = np.array(a)
    y = np.array(b)
    return np.linalg.norm(x - y)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        x_limit = float(sys.argv[1])
        y_limit = float(sys.argv[2])
        min_k = int(sys.argv[3])
        max_k = int(sys.argv[4])
        num_cluster_lower = int(sys.argv[5])
        num_cluster_upper = int(sys.argv[6])
        visit_time = int(sys.argv[7])
    else:
        min_k = 3
        max_k = 3
        x_limit = 1
        y_limit = 1
        num_cluster_lower = 11
        num_cluster_upper = 15
        visit_time = 2
    
    for num_clusters in range(num_cluster_lower, num_cluster_upper + 1):
        print(str(num_clusters) + "_" + str(min_k) + "_" + str(visit_time) + " begins")
        struct = gen_rand_TPP(num_clusters, min_k, max_k, x_limit, y_limit, visit_time)
        distance_matrix = struct[0]
        cluster = struct[1]
        dup = struct[2]
        ret = trans_to_GTSP(distance_matrix, cluster, dup)
        
        # write instance for WTSP
        input_file_name = "TPP_input" + "_" + str(num_clusters)
        write_WTSP_instance(distance_matrix, cluster, dup, input_file_name)
        # write instance for GLNS
        write_tpp_file_to_glns(ret[0], ret[1], input_file_name)
        print(str(num_clusters) + " ends")