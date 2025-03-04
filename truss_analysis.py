
import sys
import os

# Get the absolute path to the project folder
project_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(project_folder)
from genetic_algorithm import fitness as ftns


all_nodes = [
    [0.0, 0, 0],
    [40.0, 40, 0],
    [80.0, 80, 0],
    [120.0, 120, 0],
    [160.0, 160, 0],
    [200.0, 200, 0],
    [240.0, 240, 0],
    [40.25, 40, 25],
    [80.36, 80, 36],
    [120.04, 120, 40],
    [160.36, 160, 36],
    [200.25, 200, 25]
]

all_connections = [
    [0.0, 40.0], [40.0, 80.0], [80.0, 120.0], [120.0, 160.0], [160.0, 200.0], [200.0, 240.0],
    
    [0.0, 40.25], [40.25, 40.0], [40.25, 80.0], [40.25, 80.36],
    [80.36, 80.0], [80.36, 120.0], [80.36, 120.04],
    [120.04, 120.0], [120.04, 160.36], [120.0, 160.36],
    [160.0, 160.36], [160.0, 200.25], [200.25, 160.36], [200.25, 200.0],
    [200.25, 240.0]
    
]


class Material:
    def __init__(self, id, E, A):
        self.id = id
        self.E = E  # Young's modulus
        self.A = A  # Cross-sectional area

class Load:
    def __init__(self, node_id, fx, fy):
        self.node_id = node_id
        self.fx = fx
        self.fy = fy

class Support:
    def __init__(self, node_id, x_support, y_support):
        self.node_id = node_id
        self.x_support = x_support
        self.y_support = y_support


MATERIAL = [Material(1, 3.027e9, 0.0016)]  # Using steel with E = 210 GPa and A = 0.01 m^2
LOADS = [Load(4, 0, -1000)] # Applying a downward force of 980 N (100kg weight) at node 6
SUPPORTS = [Support(1, True, True), Support(7, False, True)]


weight, truss_failure_force, all = ftns.calc_fitness(all_connections, all_nodes, 0.1, 0.066e9, 3.027e9, MATERIAL, LOADS, SUPPORTS, 0.04)
print("weight: ", weight, "failure_force:", truss_failure_force, "\nf", all)
