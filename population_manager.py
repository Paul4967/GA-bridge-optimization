# https://youtu.be/qUeud6DvOWI?si=MDvBcHsIlpwnEP_T&t=420
# https://www.w3schools.com/python/python_modules.asp
# can contain arrays, objects, variables, functions, ...

import initialization
import mutation
import json
import time
import copy
import crossover
import importlib
importlib.reload(crossover)
import fitness as ftns

start_time = time.perf_counter()

## pass params like build domain, ... via functions -> or is feather / parquet more efficient? -> when will it be loaded? every time the function is called?


### Initialization

# Parameters to pass:

'''
base = {
    "nodes": [
        [0.0, 0, 0],
        [2.0, 2, 0],
        [4.0, 4, 0],
        [6.0, 6, 0],
        # ["b1", 0, 0],
        # ["b2", 2, 0],
        # ["b3", 4, 0],
        # ["b4", 6, 0],
    ],
    "connections": [
        [0.0, 2.0],
        [2.0, 4.0],
        [4.0, 6.0]
    ]
}

bridge = {
    "nodes": [
        [1.1, 1, 1],
        [3.1, 3, 1],
        [5.1, 5, 1],
        # [2.1, 2, 1]
    ],
    "connections": [
        [0.0, 1.1],
        [2.0, 1.1],
        [2.0, 3.1],
        #[4.0, 3.1],
        [4.0, 5.1],
        [6.0, 5.1],
        [1.1, 3.1],
        [3.1, 5.1]
    ]
}













mutate_node_probability = 1
mutate_connection_probability = 1
max_node_offset_multiplier = 1
grid_size = 1
build_area = 6, 3
bridge_nodes = bridge["nodes"]
base_nodes = base["nodes"]
bridge_connections = bridge["connections"]
base_connections = base["connections"]
max_mutation_amplifier = 1
min_mutation_amplifier = 1
all_connections = bridge_connections + base_connections
all_nodes = bridge_nodes + base_nodes


for _ in range(100):
    bridge_connections_copy = copy.deepcopy(bridge_connections)
    bridge_nodes_copy = copy.deepcopy(bridge_nodes)
    all_connections_copy = copy.deepcopy(all_connections)
    all_nodes_copy = copy.deepcopy(all_nodes)

    bridge_connections_, bridge_nodes_ = mutation.mutate(
        mutate_node_probability, mutate_connection_probability, max_node_offset_multiplier, grid_size, build_area,
        bridge_nodes_copy, base_nodes, bridge_connections_copy, base_connections, max_mutation_amplifier, min_mutation_amplifier, all_connections_copy, all_nodes_copy
    )




all_connections = base_connections + bridge_connections_
all_nodes = base_nodes + bridge_nodes_



'''


### START ### ------------------------------------------------------------------------------
base_nodes = [[0.0, 0, 0], [2.0, 2, 0], [4.0, 4, 0], [6.0, 6, 0]]
base_connections = [[0.0, 2.0], [2.0, 4.0], [4.0, 6.0]]
# Forces, ...



### INITIALIZATION ###
build_area = 6, 2
grid_size = 1
population_size = 10

min_node_percentage = 0.2
max_node_percentage = 0.3

population = [] # all bridges (bridge_nodes + )

for _ in range(population_size):
    bridge_nodes, bridge_connections = initialization.initialize(base_nodes, base_connections, min_node_percentage, max_node_percentage, build_area)
    population.append((bridge_nodes, bridge_connections))
    
print("POPULATION: ", population)




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

    # aktuell: 1 child pro Brücke
    for _ in range(2):
        bridge_nodes, bridge_connections = crossover.crossover(base_nodes, base_connections, bridge1_nodes, bridge2_nodes, bridge1_connections, bridge2_connections)
        population_post_crossover.append((bridge_nodes, bridge_connections))
        print(f'CN: {bridge_nodes} \n CC: {bridge_connections}')



### MUTATION ### ---------------------------------------------------------------- #everything working above

mutate_node_probability = 0.5
mutate_connection_probability = 0.5
max_node_offset_multiplier = 1
max_mutation_amplifier = 1
min_mutation_amplifier = 1

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

population_with_fitness = []
print("CALCULATING FITNESS ------------------")

for individual in population_post_mutation: # change to mutation
    bridge_nodes, bridge_connections = individual
    all_nodes = base_nodes + bridge_nodes
    all_connections = base_connections + bridge_connections

    print("all_nodes: ", all_nodes)
    print("all_connections: ", all_connections)

    fitness, weight, max_force = ftns.calc_fitness(copy.deepcopy(all_connections), copy.deepcopy(all_nodes))

    population_with_fitness.append((bridge_nodes, bridge_connections, fitness))
    print(fitness, weight, max_force)
    time.sleep(1)

# sometimes a connection id is not existing in all_nodes ex.: 6.1 in connections, and 6.2 in nodes -> bc of move_node_mutation?
# without mutation: sometimes working, but singular matrix error -> has to do something with the population strings

### SELECTION ### ------------------------------------------------------------------------




print("POPULATION POST MUTATION: ", population_post_mutation)
print("POP", population_with_fitness)





















### END ### -----------------------------------------------------------

end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Execution time: {elapsed_time:.6f} seconds")

### EXPORT ### --------------------------------------------------------

all_nodes = bridge_nodes + base_nodes
all_connections = base_connections + bridge_connections


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
