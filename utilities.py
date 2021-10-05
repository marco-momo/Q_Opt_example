from collections import defaultdict
import numpy as np

def are_the_list_equal(e, edge):
    flag = 0
    if e[0]==edge[0]:
        if e[1] == edge[1]:
            flag = 1
    return flag


def edges_in_path(edge, path):
    edges = []
    for i in range(0,len(path)-1):
        edges.append((path[i], path[i+1]))
    flag = 0
    for e in edges:
        flag = are_the_list_equal(e, edge)
        if flag:
            break
    return flag

def define_problem_variables(N):
    # paths is a list of N list, each with thre proposed paths
    I = np.zeros((N,3))
    cntr = 0
    variables = []
    variable_to_index = {}
    for i in range(0,N):
        for j in range(0,3):
            I[i,j] = cntr
            cntr += 1
            variables.append(f"q_{i}{j}")
            variable_to_index[f"q_{i}{j}"] = (i,j)
    return variables, I, variable_to_index


def define_Q_matrix(edges, I, paths, lambda_scalar, path_weigths):
    Q = defaultdict(lambda : 0)
    # diagonal elements
    for i in range(0, I.shape[0]):
        for j in range(0, I.shape[1]):
            # print(f"Car {i} choose path {j} ({paths[i][j]})")
            for e in edges:
                # print(f"edge : {e}")
                if edges_in_path(e, paths[i][j]):
                    # print("THE CODE ENTER THE IF\n")
                    Q[(f"q_{i}{j}", f"q_{i}{j}")] += 1
            Q[(f"q_{i}{j}", f"q_{i}{j}")] = Q[(f"q_{i}{j}", f"q_{i}{j}")]- lambda_scalar
            Q[(f"q_{i}{j}", f"q_{i}{j}")] += path_weigths[j]
    # off diagonal elements
    for i1 in range(0, I.shape[0]):
        for j1 in range(0, I.shape[1]):
            for i2 in range(0, I.shape[0]):
                for j2 in range(0, I.shape[1]):
                    if I[i2,j2]>I[i1,j1]:
                        # upper triangular terms
                        # print(f"Car {i1} choose path {j1} ({paths[i1][j1]})")
                        # print(f"Car {i2} choose path {j2} ({paths[i2][j2]})")
                        for e in edges:
                            # print(f"edge : {e}")
                            if edges_in_path(e, paths[i1][j1]):
                                if edges_in_path(e, paths[i2][j2]):
                                    # print("THE CODE ENTER THE IF\n")
                                    Q[(f"q_{i1}{j1}", f"q_{i2}{j2}")] += 2
    # off diagonal constraints
    for i in range(0, I.shape[0]):
        for j in range(0, I.shape[1]):
            for j2 in range(j+1, I.shape[1]):
                Q[(f"q_{i}{j}", f"q_{i}{j2}")] += 2*lambda_scalar
    return Q

