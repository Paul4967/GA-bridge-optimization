
import sys
import os

# Get the absolute path to the project folder
project_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(project_folder)
from genetic_algorithm import fitness_reworked as ftns



all_nodes = [
    [0.0, 0, 0],
    [40.0, 40, 0],
    [80.0, 80, 0],
    [120.0, 120, 0],
    [160.0, 160, 0],
    [200.0, 200, 0],
    [240.0, 240, 0],
    
    [40.04, 40, 40],
    [80.04, 80, 40],
    [120.04, 120, 40],
    [160.04, 160, 40],
    [200.04, 200, 40],
    
    [40.02, 40, 20], [80.02, 80, 20], [120.02, 120, 20], [160.02, 160, 20], [200.02, 200, 20]
]

all_connections = [
    [0.0, 40.0], [40.0, 80.0], [80.0, 120.0], [120.0, 160.0], [160.0, 200.0], [200.0, 240.0],
    
    [0.0, 40.04], [40.0, 40.04], [40.04, 80.04], [80.04, 80.0], 
    [80.04, 120.04], [120.04, 120.0],
    [120.04, 160.04], [160.04, 160.0], [200.0, 200.04],
    [160.04, 200.04], [200.04, 240.0],
    
    [40.02, 80.0], [40.02, 80.04], [80.02, 120.0], [80.02, 120.04], [120.0, 160.02], [120.04, 160.02],
    [200.02, 160.0], [200.02, 160.04]
    
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
print("weight: ", weight, "failure_force:", "a", "\nf", all)













"""

### SORT FINAL SOLUTIONS:
data_folder = os.path.join(project_folder, 'data')
file_path = os.path.join(data_folder, 'final_solutions.json')


import json

import json

# Load JSON data
# Load JSON data
with open(file_path, "r") as file:
    data = json.load(file)

# Sort the entries by ascending weight
data.sort(key=lambda x: float(x["weight"]) if str(x["weight"]).lower() != "infinity" else float('inf'))

# Update step values sequentially
for index, entry in enumerate(data, start=1):
    entry["step"] = index

# Save the sorted data back to the JSON file
with open(file_path, "w") as file:
    json.dump(data, file, indent=4)

"""