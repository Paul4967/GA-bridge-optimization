
import numpy as np
import math
import json
import os
import sys

project_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
data_folder = os.path.join(project_folder, 'data')
file_path = os.path.join(data_folder, 'pareto_fronts.json')
# population: bridge_nodes, bridge_connections

def pareto_fronts(individuals):

    # logic for removing indetermineable trusses
    individuals = [individual for individual in individuals if individual[1] != 0 and individual[2] != 0]
    individuals = [individual for individual in individuals if not math.isnan(individual[1]) and not math.isnan(individual[2])] # FILTER NaN

    
    # logic for deleting duplicates
    seen = set()
    filtered_individuals = []

    for index, failure_force, weight in individuals:
        key = (failure_force, weight)
        if key not in seen:
            seen.add(key)
            filtered_individuals.append((index, failure_force, weight))
    individuals = filtered_individuals
    

    ### START MAIN PROCESS ### --------------------
    fronts = []
    while individuals: # individuals list is not empty
        non_dominated = []  # Collect non-dominated individuals

        # check for any individual if it is dominated by any other individual -> repeat for each front
        for individual in individuals:
            is_dominated = False
            for other in individuals:
                if other == individual:
                    continue  # Skip comparing to itself

                _, individual_failure_force, individual_weight = individual
                _, other_failure_force, other_weight = other

                # check if individual is being dominated by 'other' #o = 1/1+other_failure_force, other_weigth    #i for individuals
                if all(o <= i for o, i in zip((1/(1+other_failure_force), other_weight), (1/(1+individual_failure_force), individual_weight))) and \
                    any(o < i for o, i in zip((1/(1+other_failure_force), other_weight), (1/(1+individual_failure_force), individual_weight))):
                        is_dominated = True
                        break
            if not is_dominated:
                non_dominated.append(individual)
     
        # Remove the current front individuals from the list
        individuals = [individual for individual in individuals if individual not in non_dominated]
        fronts.append(non_dominated)


    # SAVE ALL FRONTS TO JSON TO PLOT IN MATPLOTLIB
    # individual format: _, failure_force, weight
    formatted_fronts = [
        [[ind[1], ind[2]] for ind in front] for front in fronts
    ]

    # Save to JSON
    # File path
    json_file = file_path

    # Load existing data if file exists
    # Load existing data if file exists
    if os.path.exists(json_file):
        with open(json_file, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}  # If file is empty or corrupted, start fresh
    else:
        data = {}

    # Ensure data structure is a dictionary
    if not isinstance(data, dict):
        data = {}

    # Determine the next entry index
    existing_entries = [int(k) for k in data.keys()] if data else []
    next_entry = max(existing_entries, default=-1) + 1  # Get next entry number

    # Save the new collection under a new entry key
    data[str(next_entry)] = formatted_fronts

    # Save back to JSON
    with open(json_file, "w") as f:
        json.dump(data, f, indent=4)



    return fronts



def crowding_distance(front):
    # sort front by weight
    num_individuals = len(front)
    
    # Initialize crowding distances to zero
    distances = [0] * num_individuals
    
    # Sort by first objective (failure_force)
    front_sorted_by_failure_force = sorted(front, key=lambda x: x[1])

    print("DEBUG __", num_individuals, front_sorted_by_failure_force, "\n\n", front)
    
    # Calculate crowding distance for failure_force
    distances[0] = distances[-1] = float('inf')  # Boundary individuals have infinite crowding distance
    for i in range(1, num_individuals - 1):
        if (front_sorted_by_failure_force[-1][1] - front_sorted_by_failure_force[0][1] == 0) or (front_sorted_by_failure_force[-1][1] - front_sorted_by_failure_force[0][1] == 0):
            distances[i] += 0
            continue

        distances[i] += (front_sorted_by_failure_force[i + 1][1] - front_sorted_by_failure_force[i - 1][1]) / \
                        (front_sorted_by_failure_force[-1][1] - front_sorted_by_failure_force[0][1])
    
    # Sort by second objective (weight)
    # front_sorted_by_weight = front_sorted_by_failure_force
    front_sorted_by_weight = sorted(front, key=lambda x: x[2])  # x[2] is the weight

    
    # Calculate crowding distance for weight
    for i in range(1, num_individuals - 1):
        if (front_sorted_by_weight[-1][1] - front_sorted_by_weight[0][1] == 0) or (front_sorted_by_weight[-1][2] - front_sorted_by_weight[0][2] == 0):
            distances[i] += 0
            continue

        distances[i] += (front_sorted_by_weight[i + 1][2] - front_sorted_by_weight[i - 1][2]) / \
                        (front_sorted_by_weight[-1][2] - front_sorted_by_weight[0][2])
        
    return distances

    
    

    


### front format: [individual, failure_force, weight]
def calc_fitness(population, failure_force, weight):
    ## INITIATE ##
    indices = list(range(len(population)))
    individuals = list(zip(indices, failure_force, weight))

    p_fronts = pareto_fronts(individuals)
    for front in p_fronts:
        print(":::::FRONT::::::: ", front)

    for front_index, front in enumerate(p_fronts, start=1): # FRONT IS SORTED BY INDEX AND NOT BY WEIGHT
        crowding_distance_values = crowding_distance(front)
        front = sorted(front, key=lambda x: x[1]) # sorting front by failure_force

        for i in range(len(front)):
            front_list = list(front[i])
            if crowding_distance_values[i] == float('inf'):
                cd_distance = 3
            else:
                cd_distance = crowding_distance_values[i]


            
            local_fitness = 1 / ((front_index * 10) - cd_distance) # the hihger, the better



            # local_fitness = (1 / (front_index * 10)) * cd_distance + 0.1 ###OTHER WAY TO IDENTIFY FIRST FRONT IN POP_MANAGER!!!
            # front[i].append(local_fitness)
            front_list.append(local_fitness) # FIX
            front[i] = tuple(front_list)  # Convert back to tuple after appending

        p_fronts[front_index - 1] = front  # Ensure p_fronts is updated with the modified front
    return p_fronts













def pareto_local_fitness(population, failure_force, weight): # failure_forces and weights!
    pareto_fronts_ftns = calc_fitness(population, failure_force, weight)

    flattened_pff = [item for sublist in pareto_fronts_ftns for item in sublist]
    ### FIX ARRAY LENGHT ### ----------------------------------

    array_lenght = len(population)
    # Identifying missing indices
    existing_indices = [item[0] for item in flattened_pff]
    full_indices = set(range(array_lenght))  # Indices should be from 0 to 8
    missing_indices = list(full_indices - set(existing_indices))

    # Adding missing items with placeholders (e.g., None or any placeholder)
    for missing_index in missing_indices:
        # Insert a tuple for the missing index with placeholder values
        flattened_pff.append((missing_index, 0, 0, 0))

    # Sort the array by index to place the tuples in correct order
    flattened_pff.sort(key=lambda x: x[0])
    sorted_pff = flattened_pff

    ### -------------------------------------------------------

    population_fitnesses = [item[-1] for item in sorted_pff]
    return population_fitnesses



def get_individual_to_vis(population, failure_force, weight):
    # get first pareto_line
    print("POPULATION:", population, "\nFAILURE FORCE: ", failure_force, "\nWEIGHT: ", weight)
    pareto_fronts_ = calc_fitness(population, failure_force, weight)
    first_front = pareto_fronts_[0]
    first_item = first_front[0]
    f_x = first_item[1]
    f_y = first_item[2]

    last_item = first_front[-1]
    l_x = last_item[1]
    l_y = last_item[2]

    # calc center (x and y)
    center_x = (f_x + l_x) / 2
    center_y = (f_y + l_y) / 2
    print("DEBUNG :::", center_x, center_y)
    print("FIRST FRONT ::::: ", first_front, "DEBUG-------------------------------------\n\n\n")

    # get closest individual to center
    min_distance = float('inf')
    for ind in first_front:
        ind_x = ind[1]
        ind_y = ind[2]
        index = ind[0]
        dist = math.sqrt(((ind_x - center_x)**2) + ((ind_y - center_y)**2))
        if dist < min_distance:
            min_distance = dist
            closest_index = index


    return closest_index


'''
population = [[1,2], [1,2], [1,2], [1,2], [1,2], [1,2], [1,2]] # population ist ja eigendlich bridge_nodes und bridge_connections
failure_force = [11, 12, 13, 14, 15, 13, 0]
weight = [5, 0, 7, 2, 3, 4, 0]
indices = list(range(len(population)))
individuals = list(zip(indices, failure_force, weight)) # index instead of population? -> then later combine all fronts and sort?
### FITNESS MUST BE IN SAME ORDER AS POPULATION ARRAY!!!
print("INDIVIDUAL TO VIS:", get_individual_to_vis(population, failure_force, weight))
print("FITNES : : : : : : : ", pareto_local_fitness(population, failure_force, weight))
print("PARETO FRONTS: ", calc_fitness(population, failure_force, weight))
'''
   
### https://www.researchgate.net/publication/330704486_Search_Acceleration_of_Evolutionary_Multi-Objective_Optimization_Using_an_Estimated_Convergence_Point





###
### DEBUG
###

"""
# Sample population: Bridge nodes and connections
population = [
    [1, 2],  # Example individual 1
    [3, 4],  # Example individual 2
    [5, 6],  # Example individual 3
    [7, 8],  # Example individual 4
    [9, 10], # Example individual 5
    [11, 12],# Example individual 6
    [13, 14],
    [2,3] # Example individual 7
]


# Failure force values (objective to maximize)
failure_force = [
    15,  # High failure force
    21,  # Higher failure force
    5,   # Low failure force
    25,  # Very high failure force
    10,  # Moderate failure force
    8,   # Low failure force
    10.001   # High failure force
]

# Weight values (objective to minimize)
weight = [
    12,  # High weight
    5,   # Low weight
    20,  # Very high weight
    8,   # Moderate weight
    12,  # High weight
    3,   # Very low weight
    12.001    # Moderate weight
]
"""

failure_force = [
    1636887.6558473099, 1585828.894101424, 1636887.6558473045, 1585828.894101424, 
    1585828.8941014218, 1585828.8941014316, 1585828.8941014286, 1585828.8941014218, 
    1585828.894101424, 1585828.8941014218, 1585828.894101415, 1585828.8941014213, 
    1585828.8941014202, 1585828.8941014144, 1585828.8941014209, 1585828.894101418, 
    1585828.894101414, 1585828.894101413, 1585828.8941014134, 1585828.894101413, 
    1585828.8941014179, 1585828.8941014118, 1585828.894101411, 1585828.894101413, 
    1585828.894101415, 1585828.894101411, 1585828.8941014123, 1585828.894101414, 
    1585828.8941014237, 1585828.8941014102, 1585828.8941014123, 1585828.8941014095, 
    1585828.8941014225, 1585828.894101418, 1585828.894101412, 1585828.894101408, 
    1585828.8941014209, 1585828.8941014095, 1585828.894101407, 1585828.8941014118, 
    1585828.894101408, 1585828.8941014195, 1585828.8941014179, 1585828.8941014172, 
    1585828.8941014179, 1636887.6558473064, 1585828.8941014262, 1585828.8941013988, 
    1585828.8941014062, 1585828.8941014202, 1636887.6558473052, 1585828.8941014225, 
    1585828.8941014318, 1393530.8244344385, 1585828.8941014062, 1585828.8941014346, 
    1636887.655847303, 1585828.8941014288, 1585828.8941014218, 1585828.8941014302, 
    1253178.587090065, 1649326.0820281552, 1585828.8941014046, 875853.9390121911
]

weight = [
    836.0432570613123, 831.4733882743956, 836.0432570613123, 835.2975441408555, 
    830.2080333502463, 837.4177877606143, 837.4177877606143, 831.4733882743955, 
    835.2975441408556, 837.4177877606143, 830.2080333502462, 837.4177877606143, 
    835.2975441408555, 830.2080333502463, 837.4177877606143, 837.4177877606143, 
    830.2080333502463, 825.9279542081265, 835.2975441408556, 830.2080333502463, 
    837.4177877606143, 835.2975441408555, 830.2080333502463, 835.2975441408556, 
    837.4177877606143, 835.2975441408556, 835.2975441408557, 837.4177877606143, 
    837.4177877606144, 835.2975441408556, 837.4177877606143, 830.2080333502463, 
    837.4177877606144, 837.4177877606144, 837.4177877606143, 830.2080333502463, 
    837.4177877606145, 835.2975441408556, 830.2080333502463, 837.4177877606143, 
    835.2975441408556, 837.4177877606145, 837.4177877606144, 837.4177877606144, 
    837.4177877606145, 843.2530114716803, 840.3494505699337, 836.2076356582878, 
    837.4177877606143, 838.229206950175, 843.2530114716803, 840.3494505699337, 
    841.5493746562785, 836.6459747094395, 837.4177877606145, 841.5493746562786, 
    843.2530114716803, 841.5493746562784, 840.3494505699337, 841.5493746562785, 
    838.8508531941142, 885.2057891890427, 924.8515958577261, 887.1680044774464
]

population = [1]*64
## warum len nur = 64?


results = pareto_local_fitness(population, failure_force, weight) #fforce, weight
for result in results:
    print("FITNESS:", result)

### fehler weil failure_force in selction negativ sein kann? -> kann eigentloich nicht!
# failure_force und weight irgendwo vertauscht!!