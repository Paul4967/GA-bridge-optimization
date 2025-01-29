### DEPENDENCIES ### ----------------------

import sys
import os

# Get the absolute path to the project folder
project_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

import json
import math
import initialization
import mutation
import time
import copy
import crossover
import ga_modules
import pareto
import importlib
import fitness as ftns
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
file_path_termination = os.path.join(data_folder, 'final_individuals.json')

# Initialize existing data lists
existing_data = []
existing_data_termination = []



# Setup Tensorboard # --------------------
current_time = time.strftime("%Y%m%d-%H%M%S")
log_dir = f"runs/fitness_metrics/{current_time}"
# Initialize the SummaryWriter with the new log directory
writer = SummaryWriter(log_dir=log_dir)




### READ INPUTS ### -----------------------

# Construct the path to input_params.json
json_file_path = os.path.join(project_folder, 'input_params.json')

# Read the JSON file
try:
    with open(json_file_path, 'r') as json_file:
        INPUT_PARAMS = json.load(json_file)
        
        # Declare constants from JSON data
        BASE_NODES = eval(INPUT_PARAMS.get("base_nodes", "[]"))  # Convert JSON string to Python list
        BASE_CONNECTIONS = eval(INPUT_PARAMS.get("base_connections", "[]"))  # Convert JSON string to Python list
        TOURNAMENT_SIZE = INPUT_PARAMS.get("tournament_size", 0)
        NUM_SELECTIONS = INPUT_PARAMS.get("num_selections", 0)
        POPULATION_SIZE = INPUT_PARAMS.get("population_size", 0)
        GRID_SIZE = INPUT_PARAMS.get("grid_size", 0.0)
        MIN_NODE_NUM = INPUT_PARAMS.get("min_node_num", 0.0)
        MAX_NODE_NUM = INPUT_PARAMS.get("max_node_num", 0.0)
        MAX_GENERATIONS = INPUT_PARAMS.get("max_generations", 0)

        MATERIAL_YIELD_STRENGHT = INPUT_PARAMS.get("material_yield_strenght", 0)
        MATERIAL_ELASTIC_MODULUS = INPUT_PARAMS.get("material_elastic_modulus", 0)
        MEMBER_WIDTH = INPUT_PARAMS.get("member_width", 0)
        # Extract materials from JSON
        MATERIAL = [
            (m["id"], m["E"], m["A"]) 
            for m in INPUT_PARAMS.get("material", [])
        ]

        # Extract loads from JSON
        LOADS = [
            (l["node_id"], l["fx"], l["fy"]) 
            for l in INPUT_PARAMS.get("loads", [])
        ]

        # Extract supports from JSON
        SUPPORTS = [
            (s["node_id"], s["x_support"], s["y_support"])
            for s in INPUT_PARAMS.get("supports", [])
        ]

        ## + yield Strenght, E Modul, diameter
        ## truss_calc: use squared members!

        # materials = [Material(1, 3.6E9, 0.0005625)]  # A = 10^-6 m^2 ? 
        # loads = [Load(3, 0, -1000)]
        # supports = [Support(1, True, True), Support(5, False, True)]

except FileNotFoundError:
    print(f"Error: {json_file_path} does not exist.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")





####################################################################
### EVOLUTION ### --------------------------------------------------

# Initialize population
    population = [
        initialization.initialize(BASE_NODES, BASE_CONNECTIONS, MIN_NODE_NUM, MAX_NODE_NUM, BUILD_AREA)
        for _ in range(POPULATION_SIZE)
    ]


for generation in range(MAX_GENERATIONS):

    ### CROSSOVER ### ----------------------------------
    pairs = [(population[i], population[i + 1]) for i in range(0, len(population), 2)]
    population_post_crossover = []

    reproduction_rate = (POPULATION_SIZE / NUM_SELECTIONS) * 2

    for (bridge1_nodes, bridge1_connections), (bridge2_nodes, bridge2_connections) in pairs:
        for _ in range(reproduction_rate):
            bridge_nodes, bridge_connections = crossover.crossover(BASE_NODES, BASE_CONNECTIONS, bridge1_nodes, bridge2_nodes, bridge1_connections, bridge2_connections)
            population_post_crossover.append((bridge_nodes, bridge_connections))


    ### MUTATION ### ----------------------------------
    '''
    FIX MUTATION SCRIPT
    '''
    population_post_mutation = []


    ### FITNESS CALCULATION ### -----------------------
    population_post_fitness = []

    population_weight = []
    population_failure_force = []

    population_fitness = []

    for individual in population_post_mutation: # change to mutation
        bridge_nodes, bridge_connections = individual
        all_nodes = BASE_NODES + bridge_nodes
        all_connections = BASE_CONNECTIONS + bridge_connections

        weight, truss_failure_force, all_failure_forces = ftns.calc_fitness(all_connections, all_nodes, GRID_SIZE, MATERIAL_YIELD_STRENGHT, MATERIAL_ELASTIC_MODULUS, MATERIAL, LOADS, SUPPORTS, MEMBER_WIDTH)#+threshold, ...

        population_weight.append(weight)
        population_failure_force.append(truss_failure_force)

        ### DETERMINE FITNESS ------------------------
        "pareto fitness" #maximize failure_force + pass to matplotlib script
        population_fitness = pareto.pareto_local_fitness(population_post_mutation, population_failure_force, population_weight)

        "display fittest individual" #new pareto script here
        index_vis = pareto.get_individual_to_vis(population_post_mutation, population_failure_force, population_weight)
        bridge_nodes_vis, bridge_connections_vis = population_post_fitness[index_vis]

    population_post_fitness = population_post_mutation #irr



    ### SELECTION ### ----------------------------------
    selected_population = selection.tournament_selection(population_post_fitness, population_fitness, TOURNAMENT_SIZE, NUM_SELECTIONS)
    population = selected_population



    ### TENSORBOARD ###
    weight = population_weight[index_vis]
    failure_force = population_failure_force[index_vis]


    # Histograms


    # Line-charts



    ###



    ### FITTEST IND TO JSON ###
