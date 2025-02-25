# https://youtu.be/qUeud6DvOWI?si=MDvBcHsIlpwnEP_T&t=420
# https://www.w3schools.com/python/python_modules.asp
# can contain arrays, objects, variables, functions, ...

import math
import initialization
import mutation
import json
import time
import copy
import os
import crossover
import ga_modules
import pareto
import importlib
importlib.reload(crossover)
import fitness as ftns
import selection
import numpy as np
import torch
import tensorflow as tf
from torch.utils.tensorboard import SummaryWriter


file_path = 'evolution_data.json' # for saving bridge_model
# Initialize existing_data as an empty list
existing_data = []

file_path_termination = 'final_individuals.json'
existing_data_termination = []

current_time = time.strftime("%Y%m%d-%H%M%S")  # Format: "20250104-084532"
log_dir = f"runs/fitness_metrics/{current_time}"

# Initialize the SummaryWriter with the new log directory
writer = SummaryWriter(log_dir=log_dir)


start_time = time.perf_counter()

### START ### ------------------------------------------------------------------------------
base_nodes = [[0.0, 0, 0], [40.0, 40, 0], [80.0, 80, 0], [120.0, 120, 0], [160.0, 160, 0]] #[100.05, 100, 50]
base_connections = [[0.0, 40.0], [40.0, 80.0], [80.0, 120.0], [120.0, 160.0]]

# base_nodes = [[0.02, 0, 20], [40.02, 40, 20], [80.02, 80, 20], [120.02, 120, 20], [160.02, 160, 20]] #[100.05, 100, 50]
# base_connections = [[0.02, 40.02], [40.02, 80.02], [80.02, 120.02], [120.02, 160.02]]
## divide by grid_size as well!^^

### Extra Node bei y = 4 oder 5
# Forces, ...


# MUTATION
mutate_node_probability = 0.4 # or lower?
mutate_connection_probability = 0.4
max_node_offset_multiplier = 1
max_mutation_amplifier = 1
min_mutation_amplifier = 1

# SELECTION
# 10?
tournament_size = 20 # hihger?
num_selections = 50


### INITIALIZATION ###

grid_size = 0.1
build_area = 16 / grid_size, 5 / grid_size # float error?

population_size = 100

min_node_percentage = 0.001 # o.2 # FIX!!!
max_node_percentage = 0.0025 # 0.6 # * grid_size, times 10 / grind_size^2?


# tf.summary.text('Population Size', f'Population Size: {population_size}', step=0)
# tf.summary.text('Tournament Size', f'Tournament Size: {tournament_size}', step=0)

population = [] # all bridges (bridge_nodes + )

for _ in range(population_size):
    bridge_nodes, bridge_connections = initialization.initialize(base_nodes, base_connections, min_node_percentage, max_node_percentage, build_area)
    population.append((bridge_nodes, bridge_connections))
    
print("POPULATION: ", population)


i  = 0
while i < 60:
    ### CROSSOVER ### 
    'PERFORM 2 Times for each pair!!!'
    # split population into pairs
    pairs = [(population[i], population[i + 1]) for i in range(0, len(population), 2)]

    population_post_crossover = []
    # Iterate through the pairs to retrieve the required elements
    for pair in pairs:
        # Unpack the pair into two bridges
        (bridge1_nodes, bridge1_connections), (bridge2_nodes, bridge2_connections) = pair
        print("PAIR: ", pair)
        print(f'BN1: {bridge1_nodes},\n BN2: {bridge2_nodes},\n BC1: {bridge1_connections},\n BC2: {bridge2_connections}')

        # aktuell: 2 childs pro Brücke
        for _ in range(4):
            bridge_nodes, bridge_connections = crossover.crossover(base_nodes, base_connections, bridge1_nodes, bridge2_nodes, bridge1_connections, bridge2_connections)
            population_post_crossover.append((bridge_nodes, bridge_connections))
            print(f'CN: {bridge_nodes} \n CC: {bridge_connections}')



    ### MUTATION ### ---------------------------------------------------------------- #everything working above
    
    population_post_mutation = []

    for individual in population_post_crossover:
        print("X15", individual, "\n ", individual[0])
        
        # Unpack the individual to reset variables from the population
        bridge_nodes, bridge_connections = copy.deepcopy(individual)

        # Ensure the base and bridge variables are isolated and reset
        bridge_connections_copy = copy.deepcopy(bridge_connections)
        bridge_nodes_copy = copy.deepcopy(bridge_nodes)

        # Recompute all_connections and all_nodes for this specific individual
        all_connections = copy.deepcopy(base_connections + bridge_connections)
        all_nodes = copy.deepcopy(base_nodes + bridge_nodes)

        # Perform mutation with fresh variables
        bridge_connections_, bridge_nodes_ = mutation.mutate(
            mutate_node_probability,
            mutate_connection_probability,
            max_node_offset_multiplier,
            grid_size,
            build_area,
            bridge_nodes_copy,
            copy.deepcopy(base_nodes),  # Ensure base_nodes are isolated
            bridge_connections_copy,
            copy.deepcopy(base_connections),  # Ensure base_connections are isolated
            max_mutation_amplifier,
            min_mutation_amplifier,
            all_connections,
            all_nodes
        )

        # Append mutated individual to the new population
        population_post_mutation.append((bridge_nodes_, bridge_connections_))




    ### FITNESS CALCULATION ### ----------------------------------------------------------- #everything above working

    population_post_fitness = []
    population_fitness = []
    population_weight = []
    population_max_force = []
    print("CALCULATING FITNESS ------------------")

    for individual in population_post_mutation: # change to mutation
        bridge_nodes, bridge_connections = individual
        all_nodes = base_nodes + bridge_nodes
        all_connections = base_connections + bridge_connections

        print("all_nodes: ", all_nodes)
        print("all_connections: ", all_connections)

        _, weight, max_force, _ = ftns.calc_fitness(copy.deepcopy(all_connections), copy.deepcopy(all_nodes))

        population_post_fitness.append((bridge_nodes, bridge_connections))
        population_weight.append(weight)
        population_max_force.append(1 / (1 + max_force)) #ACTUALLY NOT MAX_FORCE, BUT FAILURE_FORCE!!!!# bc it should be maximized
        # wrong fitness: population_fitness.append(fitness)
    
    ## get population local fitness                                              
    population_fitness = pareto.pareto_local_fitness(population_post_mutation, population_max_force, population_weight)

        

    # sometimes a connection id is not existing in all_nodes ex.: 6.1 in connections, and 6.2 in nodes -> bc of move_node_mutation?
    # without mutation: sometimes working, but singular matrix error -> has to do something with the population strings

    ### DISPLAY FITTEST INDIVIDUAL ### ------------------------------------------------------_

    max_fitness_index = population_fitness.index(max(population_fitness)) ###OLD

    index_vis = pareto.get_individual_to_vis(population_post_mutation, population_max_force, population_weight)
    bridge_nodes_vis, bridge_connections_vis = population_post_fitness[index_vis]




    ### SELECTION ### ------------------------------------------------------------------------

    selected_population = selection.tournament_selection(population_post_fitness, population_fitness, tournament_size, num_selections)


    ## CYCLE ##
    population = selected_population


    ### TENSORBOARD ###
    print("POPULATION POST MUTATION: ", population_post_mutation)
    print("POP", population_post_fitness)
    print("FITNESS: ", population_fitness)
    print("SEL P:", selected_population)


    
    #### REPLACED max_fitness_index with index_vis #### ----

    print("FITNESS: ", population_fitness[max_fitness_index])
    print("WEIGHT: ", population_weight[index_vis])
    print("MAX FORCE: ", population_max_force[index_vis])

    i += 1
    fitness = population_fitness[max_fitness_index]
    weight = population_weight[index_vis]
    max_force = population_max_force[index_vis] #old?

    population_fitness_variance = np.var(population_fitness)

    """TEMPORARY!"""
    max_force = (1 - max_force) / max_force


    ## TENSORBOARD ADD HISTOGRAMS
    population_weight_ = [value for value in population_weight if value != 0]
    population_max_force_ = [value for value in population_max_force if value != 0 and value <= 10000]
    population_weight_tensor = torch.tensor(population_weight_)
    population_max_force_tensor = torch.tensor(population_max_force_)

    # Log these values (you can use the iteration number as a step)
    step = i  # Replace with your actual iteration or epoch number
    # writer.add_scalar("Metrics/Fitness", fitness, step)
    writer.add_scalar("Metrics/Fittest Individual Weight", weight, step)
    writer.add_scalar("Metrics/Fittest Individual Max Force", max_force, step)
    # writer.add_scalar("Metrics/Population Fitness Variance", population_fitness_variance, step)
    writer.add_histogram("population_weight", population_weight_tensor, step)
    if population_max_force_:
        writer.add_histogram("population_max_force", population_max_force_tensor, step) # remove all values greater than 10kn
    writer.flush()

    # time.sleep(.1)

    ### GET ALL FORCES OF FITTEST INDIVIDUAL
    all_connections_vis = base_connections + bridge_connections_vis
    all_nodes_vis = base_nodes + bridge_nodes_vis
    _, _, _, forces = ftns.calc_fitness(all_connections_vis, all_nodes_vis)
    print("FORCES1 : : : ", forces)
    forces = [float(f) for f in forces] # fixed?
    print("FORCES2 : : : ", forces)
    weight_vis = ga_modules.calc_weight(all_connections_vis, all_nodes_vis)
    # convert NaN to 0 in forces:
    # forces = [0 if str(f) == 'NaN' else f for f in forces] # not working!!!
    # VISUALIZE FITTEST INDIVIDUAL: -> each run needs a unique json
    data = {
        "step": i,
        "all_connections": all_connections_vis,
        "all_nodes": all_nodes_vis,
        "forces": forces,
        #"population_fitness": population_fitness
        "max_force": max([abs(force) for force in forces]),
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

    print(f"Data for step {i} appended to {file_path}")
    # time.sleep(5)



    ### END OF ITERATION ### ---------------------------------------------------------------------------------------------


### END ### -----------------------------------------------------------
writer.close()

end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Execution time: {elapsed_time:.6f} seconds")



### SAVE FINAL PARETO FRONT ###
# get front -> all individuals with fitness higher or equal to 0.1
step = 0
for i, individual in enumerate(population_post_fitness):
    
    if population_fitness[i] >= 0.1:
        bridge_nodes_front, bridge_connections_front = individual
        all_connections_front = base_connections + bridge_connections_front
        all_nodes_front = base_nodes + bridge_nodes_front
        step += 1

        _, _, _, forces = ftns.calc_fitness(all_connections_front, all_nodes_front)
        forces = [float(f) for f in forces] # fixed?
        weight_front = ga_modules.calc_weight(all_connections_front, all_nodes_front)

        # add to json
        data = {
            "step": step,
            "all_connections": all_connections_front,
            "all_nodes": all_nodes_front,
            "forces": forces,
            "population_fitness": 1,
            "max_force": max([abs(force) for force in forces]),
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

    




# Launch Tensorboard:
# python -m tensorboard.main --logdir=runs/fitness_metrics
# or:
# python -m tensorboard.main --logdir=runs/fitness_metrics --reload_interval=2














'''
### EXPORT ### --------------------------------------------------------

all_nodes =  base_nodes + bridge_nodes_vis
all_connections = base_connections + bridge_connections_vis


data = {
    "all_connections": all_connections,
    "all_nodes": all_nodes
}

# Save the data to a json file
file_path = 'connections_and_nodes.json'
with open(file_path, 'w') as f:
    json.dump(data, f)

file_path

print("saved to file")



### LOG POPULATION VARIANCE TO TENSORBOARD AS WELL!!!
### AND FORCE VARIANCE!!!
### AND DISPLAY FORCE VARIANCE IN CHART!

'''