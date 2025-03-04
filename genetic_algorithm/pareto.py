
import numpy as np
import math
import json
import os
import sys

project_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
data_folder = os.path.join(project_folder, 'data')
file_path = os.path.join(data_folder, 'pareto_fronts.json')
# population: bridge_nodes, bridge_connections

def pareto_fronts(individuals, save_fronts):

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

    ### save fronts to mathplotlib ### ---------------
    # individual format: _, failure_force, weight
    formatted_fronts = [
        [[ind[1], ind[2]] for ind in front] for front in fronts
    ]

    # Save to JSON
    save_fronts = False
    if save_fronts and 1 == 2:
        # File path
        json_file = file_path

        # Load existing data if file exists
        if os.path.exists(json_file):
            with open(json_file, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
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
            json.dump(data, f)

    return fronts


def crowding_distance(front):
    # sort front by weight
    num_individuals = len(front)
    
    # Initialize crowding distances to zero
    distances = [0] * num_individuals
    
    # Sort by first objective (failure_force)
    front_sorted_by_failure_force = sorted(front, key=lambda x: x[1])
    
    # Calculate crowding distance for failure_force
    distances[0] = distances[-1] = float('inf') #only boundary solutions
    for i in range(1, num_individuals - 1):
        if (front_sorted_by_failure_force[-1][1] - front_sorted_by_failure_force[0][1] == 0) or (front_sorted_by_failure_force[-1][1] - front_sorted_by_failure_force[0][1] == 0):
            distances[i] += 0
            continue

        distances[i] += (front_sorted_by_failure_force[i + 1][1] - front_sorted_by_failure_force[i - 1][1]) / \
                        (front_sorted_by_failure_force[-1][1] - front_sorted_by_failure_force[0][1])
    
    # Sort by second objective (weight)
    front_sorted_by_weight = sorted(front, key=lambda x: x[2])  # x[2] is the weight
    
    # Calculate crowding distance for weight
    for i in range(1, num_individuals - 1):
        if (front_sorted_by_weight[-1][1] - front_sorted_by_weight[0][1] == 0) or (front_sorted_by_weight[-1][2] - front_sorted_by_weight[0][2] == 0):
            distances[i] += 0
            continue

        distances[i] += (front_sorted_by_weight[i + 1][2] - front_sorted_by_weight[i - 1][2]) / \
                        (front_sorted_by_weight[-1][2] - front_sorted_by_weight[0][2])
        
    return distances


def calc_fitness(population, failure_force, weight, save_fronts):
    ## INITIATE ##
    indices = list(range(len(population)))
    individuals = list(zip(indices, failure_force, weight))

    p_fronts = pareto_fronts(individuals, save_fronts)
    for front in p_fronts:
        print(":::::FRONT::::::: ", front)

    for front_index, front in enumerate(p_fronts, start=1):
        crowding_distance_values = crowding_distance(front)
        front = sorted(front, key=lambda x: x[1]) # sorting front by failure_force

        for i in range(len(front)):
            front_list = list(front[i])
            if crowding_distance_values[i] == float('inf'):
                cd_distance = 3
            else:
                cd_distance = crowding_distance_values[i]

            local_fitness = 1 / ((front_index * 10) - cd_distance) # the hihger, the better

            front_list.append(local_fitness)
            front[i] = tuple(front_list)

        p_fronts[front_index - 1] = front
    return p_fronts


def pareto_local_fitness(population, failure_force, weight, save_fronts): # failure_forces and weights!
    pareto_fronts_ftns = calc_fitness(population, failure_force, weight, save_fronts)

    flattened_pff = [item for sublist in pareto_fronts_ftns for item in sublist]
    ### FIX ARRAY LENGHT ### ----------------------------------

    array_lenght = len(population)
    # Identifying missing indices
    existing_indices = [item[0] for item in flattened_pff]
    full_indices = set(range(array_lenght))
    missing_indices = list(full_indices - set(existing_indices))

    # Adding missing items with placeholders
    for missing_index in missing_indices:
        # Insert a tuple for the missing index with placeholder values
        flattened_pff.append((missing_index, 0, 0, 0))

    # Sort the array by index to place the tuples in correct order
    flattened_pff.sort(key=lambda x: x[0])
    sorted_pff = flattened_pff

    ### -------------------------------------------------------
    population_fitnesses = [item[-1] for item in sorted_pff]
    return population_fitnesses


def get_individual_to_vis(population, failure_force, weight, save_fronts):
    # get first pareto_line
    print("POPULATION:", population, "\nFAILURE FORCE: ", failure_force, "\nWEIGHT: ", weight)
    pareto_fronts_ = calc_fitness(population, failure_force, weight, save_fronts)
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
