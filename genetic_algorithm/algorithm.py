### DEPENDENCIES ### ----------------------

import sys
import os

# Get the absolute path to the project folder
project_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(project_folder)
import json
import math
import random
import initialization_reworked as initialization
#import mutation_reworked as mutation
import m_r as mutation
import time
import copy
import crossover
import ga_modules
import pareto_reworked as pareto
import importlib
import fitness_reworked as ftns
import selection
import numpy as np
import torch
import tensorflow as tf
from torch.utils.tensorboard import SummaryWriter

# -----------------------------------------


### SETUP ### -----------------------------

# Construct the paths to the data folder and the JSON files
data_folder = os.path.join(project_folder, 'data')

# Ensure the 'data' folder exists, if not, create it
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Define the full file paths for saving the data
file_path = os.path.join(data_folder, 'evolution_data.json')
file_path_termination = os.path.join(data_folder, 'final_solutions.json')
file_pareto_path = os.path.join(data_folder, "first_pareto_fronts.json")

# Initialize existing data lists
existing_data = []
existing_pareto_data = []
existing_data_termination = []



# Setup Tensorboard # --------------------
current_time = time.strftime("%Y%m%d-%H%M%S")
log_dir = f"runs/fitness_metrics/{current_time}"
# Initialize the SummaryWriter with the new log directory
writer = SummaryWriter(log_dir=log_dir)


### TRUSS_CALC_SETUP
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



### READ INPUTS ### -----------------------

# Construct the path to input_params.json
json_file_path = os.path.join(project_folder, 'input_params.json')

# Read the JSON file
try:
    with open(json_file_path, 'r') as json_file:
        INPUT_PARAMS = json.load(json_file)
        
        # Declare constants from JSON data
        BASE_NODES = INPUT_PARAMS.get("base_nodes", "[]")  # Convert JSON string to Python list
        BASE_CONNECTIONS = INPUT_PARAMS.get("base_connections", "[]")  # Convert JSON string to Python list
        TOURNAMENT_SIZE = INPUT_PARAMS.get("tournament_size", 0)
        NUM_SELECTIONS = INPUT_PARAMS.get("num_selections", 0)
        POPULATION_SIZE = INPUT_PARAMS.get("population_size", 0)
        GRID_SIZE = INPUT_PARAMS.get("grid_size", 0.0)
        BUILD_AREA_ = INPUT_PARAMS.get("build_area", "[]")
        BUILD_AREA = BUILD_AREA_[0] / GRID_SIZE, BUILD_AREA_[1] / GRID_SIZE
        MIN_NODE_NUM = INPUT_PARAMS.get("min_node_num", 0.0)
        MAX_NODE_NUM = INPUT_PARAMS.get("max_node_num", 0.0)
        MAX_GENERATIONS = INPUT_PARAMS.get("max_generations", 0)

        MATERIAL_YIELD_STRENGHT = INPUT_PARAMS.get("material_yield_strenght", 0)
        MATERIAL_ELASTIC_MODULUS = INPUT_PARAMS.get("material_elastic_modulus", 0)
        MEMBER_WIDTH = INPUT_PARAMS.get("member_width", 0)
        # Extract materials from JSON
        MATERIAL = [
            Material(m["id"], m["E"], m["A"] / GRID_SIZE**2)
            for m in INPUT_PARAMS.get("material", []) #Divide A by GRID_SIZE^2
        ]

        # Extract loads from JSON
        LOADS = [
            Load(l["node_id"], l["fx"], l["fy"])  # Correct way to instantiate a class
            for l in INPUT_PARAMS.get("loads", [])
        ]

        # Extract supports from JSON
        SUPPORTS = [
            Support(s["node_id"], s["x_support"], s["y_support"])
            for s in INPUT_PARAMS.get("supports", [])
        ]

except FileNotFoundError:
    print(f"Error: {json_file_path} does not exist.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")



####################################################################
def is_viable(bn, BN, bc, BC, GRID_SIZE, MATERIAL_YIELD_STRENGHT, 
    MATERIAL_ELASTIC_MODULUS, MATERIAL, LOADS, SUPPORTS, MEMBER_WIDTH):

    all_connections = BC + bc
    all_nodes = BN + bn

    weight, truss_failure_force, _ = ftns.calc_fitness(
        all_connections, all_nodes, GRID_SIZE, MATERIAL_YIELD_STRENGHT, 
        MATERIAL_ELASTIC_MODULUS, MATERIAL, LOADS, SUPPORTS, MEMBER_WIDTH
    )
    if weight != 0 and truss_failure_force != 0:
        return True






### INITIALIZATION ### ---------------------------------------------
population_RT = []
a = 0
while len(population_RT) < (POPULATION_SIZE):
    ind = initialization.initialize(BASE_NODES, BASE_CONNECTIONS, MIN_NODE_NUM, MAX_NODE_NUM, BUILD_AREA)

    all_connections = BASE_CONNECTIONS + ind[1]
    all_nodes = BASE_NODES + ind[0]

    weight, truss_failure_force, _ = ftns.calc_fitness(
        all_connections, all_nodes, GRID_SIZE, MATERIAL_YIELD_STRENGHT, 
        MATERIAL_ELASTIC_MODULUS, MATERIAL, LOADS, SUPPORTS, MEMBER_WIDTH
    )

    if weight != 0 and truss_failure_force != 0:
        a +=1
        population_RT.append(ind)  # guarantee all individuals are viable





### EVOLUTION START #################################################
for i, generation in enumerate(range(MAX_GENERATIONS), 1):


    ### FITNESS ### -------------------------------------------------
    population_weight = []
    population_failure_force = []
    population_RT_fitness = [] #irr

    # calculate objective values
    for individual in population_RT:
        all_nodes = BASE_NODES + individual[0]
        all_connections = BASE_CONNECTIONS + individual[1]

        weight, truss_failure_force, _ = ftns.calc_fitness(all_connections, all_nodes, GRID_SIZE, MATERIAL_YIELD_STRENGHT, MATERIAL_ELASTIC_MODULUS, MATERIAL, LOADS, SUPPORTS, MEMBER_WIDTH)
        
        population_weight.append(weight)
        population_failure_force.append(abs(truss_failure_force))

    # calculate pareto fitness (sorted by front and cd dist.)
    population_RT_fitness = pareto.pareto_local_fitness(population_RT, population_failure_force, population_weight)

    "display fittest individual"
    index_vis = pareto.get_individual_to_vis(population_RT, population_failure_force, population_weight)
    bridge_nodes_vis, bridge_connections_vis = population_RT[index_vis]
    population_vis = population_RT



    "Removing duplicates:"
    "delete all fitness values and corresponding individuals with a fitness of 0"
    """
    # Filter out individuals with fitness == 0
    population_RT, population_RT_fitness = zip(
        *[(ind, fit) for ind, fit in zip(population_RT, population_RT_fitness) if fit != 0]
    )
    # Convert back to lists (since zip returns tuples)
    population_RT = list(population_RT)
    population_RT_fitness = list(population_RT_fitness)
    """
    # already completed inside of pareto function


    ### OFFSPRING OPERATIONS ### ------------------------------------

    ### Select PT (50% of RT)
    population_PT, population_PT_fitness = selection.select_PT(population_RT, population_RT_fitness, POPULATION_SIZE)
    
    ### Create offspring (using tournament selection)
    population_PT_offspring = selection.crowded_tournament_selection(population_PT, population_PT_fitness, TOURNAMENT_SIZE, POPULATION_SIZE / 4)

    "set worst 50% to be offspring population?"



    ### CROSSOVER ###----------------
    population_PT_offspring_mated = []

    random.shuffle(population_PT_offspring)
    pairs = [(population_PT_offspring[i], population_PT_offspring[i + 1]) for i in range(0, len(population_PT_offspring), 2)]

    reproduction_rate = 4 # 2 childs per individual

    for (bridge1_nodes, bridge1_connections), (bridge2_nodes, bridge2_connections) in pairs:
        for _ in range(int(reproduction_rate)):

            num_viable = 0
            while num_viable < 1: #guarantee all solutions are viable

                bridge_nodes, bridge_connections = crossover.crossover(BASE_NODES, BASE_CONNECTIONS, bridge1_nodes, bridge2_nodes, bridge1_connections, bridge2_connections)

                if is_viable(bridge_nodes, BASE_NODES, bridge_connections, BASE_CONNECTIONS, GRID_SIZE, MATERIAL_YIELD_STRENGHT, 
                    MATERIAL_ELASTIC_MODULUS, MATERIAL, LOADS, SUPPORTS, MEMBER_WIDTH):

                    num_viable +=1
                    population_PT_offspring_mated.append((bridge_nodes, bridge_connections))





    ### MUTATION ###---------------------
    population_PT_offspring_mutated = []

    for individual in population_PT_offspring_mated:

        ind_is_viable = False
        while ind_is_viable is False:

            # Unpack the individual to reset variables from the population
            bridge_nodes, bridge_connections = copy.deepcopy(individual)

            # Ensure the base and bridge variables are isolated and reset
            bridge_connections_copy = copy.deepcopy(bridge_connections)
            bridge_nodes_copy = copy.deepcopy(bridge_nodes)

            # Recompute all_connections and all_nodes for this specific individual
            all_connections = copy.deepcopy(BASE_CONNECTIONS + bridge_connections)
            all_nodes = copy.deepcopy(BASE_NODES + bridge_nodes)

            mutation_rate = 0.2
            max_node_offset_multiplier = 1
            # Perform mutation with fresh variables
            bridge_connections_, bridge_nodes_ = mutation.mutate(
                mutation_rate,
                max_node_offset_multiplier,
                GRID_SIZE,
                BUILD_AREA,
                bridge_nodes_copy,
                copy.deepcopy(BASE_NODES),  # Ensure base_nodes are isolated
                bridge_connections_copy,
                copy.deepcopy(BASE_CONNECTIONS),  # Ensure base_connections are isolated
                all_connections,
                all_nodes
            )

            if is_viable(bridge_nodes, BASE_NODES, bridge_connections, BASE_CONNECTIONS, GRID_SIZE, MATERIAL_YIELD_STRENGHT, 
                    MATERIAL_ELASTIC_MODULUS, MATERIAL, LOADS, SUPPORTS, MEMBER_WIDTH):
                
                ind_is_viable = True

        
        population_PT_offspring_mutated.append((bridge_nodes_, bridge_connections_))
                

    


    ### recombine offspring and parents ### -----------------------------
    population_QT = population_PT_offspring_mutated
    population_RT = population_PT + population_QT



    # further todo: tensorboard + jsons + ind to vis
    # + selection prevent selecting same ind twice?
    # + sort out duplicates in pareto?

















    ### TENSORBOARD ###

    weight = population_weight[index_vis]
    failure_force = population_failure_force[index_vis]


    population_weight_ = [value for value in population_weight if value != 0]
    population_failure_force_ = [value for value in population_failure_force if value != 0]
    population_weight_tensor = torch.tensor(population_weight_)
    population_failure_force_tensor = torch.tensor(population_failure_force_)

    step = i 
    writer.add_scalar("Metrics/Avg. ind. Weight", weight, step)
    writer.add_scalar("Metrics/Avg. ind. Failure Force", failure_force, step)
    # writer.add_scalar("Metrics/Population Fitness Variance", population_fitness_variance, step)
    writer.add_histogram("population_weight", population_weight_tensor, step)
    if population_failure_force_:
        writer.add_histogram("population_max_force", population_failure_force_tensor, step) # remove all values greater than 10kn
    writer.flush()

    


    ### FITTEST IND TO JSON ###
    all_connections_vis = BASE_CONNECTIONS + bridge_connections_vis
    all_nodes_vis = BASE_NODES + bridge_nodes_vis
    _, _, all_failure_forces = ftns.calc_fitness(all_connections_vis, all_nodes_vis, GRID_SIZE, MATERIAL_YIELD_STRENGHT, MATERIAL_ELASTIC_MODULUS, MATERIAL, LOADS, SUPPORTS, MEMBER_WIDTH)
    all_failure_forces = [float(f) for f in all_failure_forces]
    weight_vis = ga_modules.calc_weight(all_connections_vis, all_nodes_vis)
    print("ALL_FAILURE_F", all_failure_forces)


    data = {
        "step": i,
        "all_connections": all_connections_vis,
        "all_nodes": all_nodes_vis,
        "failure_forces": all_failure_forces,
        "min_failure_force": min([abs(failure_force) for failure_force in all_failure_forces]),
        "weight": weight_vis
    }

    # Load existing data
    if os.stat(file_path).st_size == 0:
        print("The file is empty!")
    else:
        with open(file_path, 'r') as f:
            existing_data = json.load(f)

    # Append new data
    existing_data.append(data)

    # Save the updated data back to the file
    with open(file_path, 'w') as f:
        # json.dump(existing_data, f, indent=4)
        json.dump(existing_data, f)



    # Save 1. Pareto Front to json
    # use step
    front_weight = []
    front_failure_force = []
    pareto_front = []
    for i, individual in enumerate(population_vis):
        if population_RT_fitness[i] >= 0.1:
            bridge_nodes_front, bridge_connections_front = individual
            all_connections_front = BASE_CONNECTIONS + bridge_connections_front
            all_nodes_front = BASE_NODES + bridge_nodes_front
            weight, failure_force, _ = ftns.calc_fitness(all_connections_front, all_nodes_front, GRID_SIZE, MATERIAL_YIELD_STRENGHT, MATERIAL_ELASTIC_MODULUS, MATERIAL, LOADS, SUPPORTS, MEMBER_WIDTH)

            pareto_front.append([weight, failure_force])
        
    # sort by weight
    pareto_front.sort(key=lambda x: x[0])

    # save to json ### ---------------------
    pareto_data = {
        "step": step,
        "pareto_front": pareto_front,
    }

    # Load existing data
    if os.stat(file_pareto_path).st_size == 0:
        print("The file is empty!")
    else:
        with open(file_pareto_path, 'r') as f:
            existing_pareto_data = json.load(f)

    # Append new data
    existing_pareto_data.append(pareto_data)

    # Save the updated data back to the file
    with open(file_pareto_path, 'w') as f:
        # json.dump(existing_data, f, indent=4)
        json.dump(existing_pareto_data, f)






###############################################################################
### TERMINATION ### -----------------------------------------------------------

### SAVE FINAL PARETO FRONT ###
step = 0
for i, individual in enumerate(population_vis):
    if population_RT_fitness[i] >= 0.1:
        bridge_nodes_front, bridge_connections_front = individual
        all_connections_front = BASE_CONNECTIONS + bridge_connections_front
        all_nodes_front = BASE_NODES + bridge_nodes_front
        step += 1

        _, _, all_failure_forces = ftns.calc_fitness(all_connections_front, all_nodes_front, GRID_SIZE, MATERIAL_YIELD_STRENGHT, MATERIAL_ELASTIC_MODULUS, MATERIAL, LOADS, SUPPORTS, MEMBER_WIDTH)
        all_failure_forces = [float(f) for f in all_failure_forces]
        weight_front = ga_modules.calc_weight(all_connections_front, all_nodes_front)

        # add to json
        data = {
        "step": step,
        "all_connections": all_connections_front,
        "all_nodes": all_nodes_front,
        "failure_forces": all_failure_forces,
        "min_failure_force": min([abs(failure_force) for failure_force in all_failure_forces]),
        "weight": weight_front
        }

        # Load existing data
        if os.stat(file_path_termination).st_size == 0:
            print("The file is empty!")
        else:
            with open(file_path_termination, 'r') as f:
                existing_data_termination = json.load(f)

        # Append new data
        existing_data_termination.append(data)

        # Save the updated data back to the file
        with open(file_path_termination, 'w') as f:
            # json.dump(existing_data, f, indent=4)
            json.dump(existing_data_termination, f)




# python -m tensorboard.main --logdir=runs/fitness_metrics --reload_interval=2