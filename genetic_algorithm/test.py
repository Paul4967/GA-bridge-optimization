### DEPENDENCIES ### ----------------------

import sys
import os

# Get the absolute path to the project folder
project_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

import json


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
            Material(m["id"], m["E"], m["A"]) 
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

print(LOADS, MATERIAL, SUPPORTS)