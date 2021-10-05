import dimod
import pandas as pd
from dimod import ExactSolver
from dwave_qbsolv import QBSolv
from tabu import TabuSampler
from utilities import *
import time
# Elapsed times
## 418  cars ---> 0.60 s
## 1000 cars ----> 3.96 s
N_FIXED = 100
N_OPT = 418
lambda_scalar = N_OPT + N_FIXED # a car be considered at most two times (the maximum length of a path is 2)

print(f"The problem has {N_OPT*3} variables")
print(f"The number of feasible solution is {2**(N_OPT*3)}")
dtab = pd.read_excel('small_graph_structure.xlsx')
# print(dtab.head())

vertices = set(list(dtab.id1)+list(dtab.id2))
# print(vertices)

edges = [(x,y) for x,y in zip(dtab.id1,dtab.id2)]
# print(edges)

paths_3 = [['origin', 'destination'], ['origin', 'a', 'destination'], ['origin', 'b','destination']]
paths = []

### Weights
path_weigths = [N_FIXED, 0, 0]

for i in range(0,N_OPT):
    paths.append([x for x in paths_3])
variables, I, variable_to_index = define_problem_variables(N_OPT)

Q = define_Q_matrix(edges, I, paths, lambda_scalar, path_weigths)
# print(dict(Q))
bqm = dimod.BQM(Q,dimod.Vartype.BINARY) # , offset = lambda_scalar*N_OPT
# response = QBSolv().sample_qubo(bqm)
# response = ExactSolver().sample_qubo(Q)
###### SOLVE THE PROBLEM ##########
start = time.time()
response = TabuSampler().sample_qubo(Q)
end = time.time()
print(f"Elapsed time : {end-start}")
# print("samples=" + str(list(response.samples())))
# print("energies=" + str(list(response.data_vectors['energy'])))
solution = response.first.sample
# print(response.first.energy)
t =0
constraints_satisfaction = np.ones(N_OPT)
path_counters = np.zeros(3)
for k,v in solution.items():
    if v == 1:
        t +=1
        idx = variable_to_index[k]
        print(f"Car {idx[0]} choose path {paths[idx[0]][idx[1]]}")
        constraints_satisfaction[idx[0]] -= 1
        path_counters[idx[1]] += 1

print(f"Total Number of Decision : {t}/{N_OPT}")
print(f"Number of satisfied constraints : {int(N_OPT - np.sum(constraints_satisfaction))}/{N_OPT}")
print(path_counters)