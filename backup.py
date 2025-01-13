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
import pareto
import importlib
import fitness as ftns
import selection
import numpy as np
# from torch.utils.tensorboard import SummaryWriter


start_time = time.perf_counter()

### START ### ------------------------------------------------------------------------------
base_nodes = [[0.0, 0, 0], [20.0, 20, 0], [40.0, 40, 0], [60.0, 60, 0], [80.0, 80, 0], [100.0, 100, 0]]
base_connections = [[0.0, 20.0], [20.0, 40.0], [40.0, 60.0], [60.0, 80.0], [80.0, 100.0]]

# base_nodes = [[0.0, 0, 0], [2.0, 2, 0], [4.0, 4, 0], [6.0, 6, 0], [8.0, 8, 0], [10.0, 10, 0]]
# base_connections = [[0.0, 2.0], [2.0, 4.0], [4.0, 6.0], [6.0, 8.0], [8.0, 10.0]]
## divide by grid_size as well!^^

# Forces, ...


# MUTATION
mutate_node_probability = 0.3
mutate_connection_probability = 0.3
max_node_offset_multiplier = 1
max_mutation_amplifier = 1
min_mutation_amplifier = 1

# SELECTION
# 10?
tournament_size = 3
num_selections = 6


### INITIALIZATION ###

grid_size = 0.1
build_area = 10 / grid_size, 3 / grid_size # float error?

population_size = 10

min_node_percentage = 0.02 # o.2
max_node_percentage = 0.06# 0.6


# tf.summary.text('Population Size', f'Population Size: {population_size}', step=0)
# tf.summary.text('Tournament Size', f'Tournament Size: {tournament_size}', step=0)

population = [] # all bridges (bridge_nodes + )

for _ in range(population_size):
    bridge_nodes, bridge_connections = initialization.initialize(base_nodes, base_connections, min_node_percentage, max_node_percentage, build_area)
    population.append((bridge_nodes, bridge_connections))
    
print("POPULATION: ", population)
time.sleep(5)



'''
i  = 0
while i < 2:
    i +=1
    
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


    ''''''
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

        fitness, weight, max_force, _ = ftns.calc_fitness(copy.deepcopy(all_connections), copy.deepcopy(all_nodes))

        population_post_fitness.append((bridge_nodes, bridge_connections))
        population_weight.append(weight)
        population_max_force.append(max_force)
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
    '''