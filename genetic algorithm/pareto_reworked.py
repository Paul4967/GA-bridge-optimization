
import numpy as np
import math

################


################
# population: bridge_nodes, bridge_connections

# failure_fore: 1/1+failure_force



def pareto_fronts(individuals):

    ### LOGIC FOR REMOVING INDETERMINABLE TRUSSES ### 
    ### -> remove from individuals
    individuals = [individual for individual in individuals if individual[1] != 0 and individual[2] != 0]
    individuals = [individual for individual in individuals if not math.isnan(individual[1]) and not math.isnan(individual[2])] # FILTER NaN

    ### START MAIN PROCESS ### --------------------

    fronts = []
    while individuals: # individuals list is not empty
        # front = []
        non_dominated = []  # Collect non-dominated individuals

        for individual in individuals:
            
            is_dominated = False
            for other in individuals:
                if other == individual:
                    continue  # Skip comparing the individual with itself

                _, individual_max_force, individual_weight = individual
                _, other_max_force, other_weight = other

                
                if all(o <= i for o, i in zip((other_max_force, other_weight), (individual_max_force, individual_weight))) and \
                    any(o < i for o, i in zip((other_max_force, other_weight), (individual_max_force, individual_weight))):
                        is_dominated = True
                        break
            if not is_dominated:
                non_dominated.append(individual)
     
        # Remove the current front individuals from the list
        individuals = [individual for individual in individuals if individual not in non_dominated]
        fronts.append(non_dominated)

    return fronts



def crowding_distance(front):
    # sort front by weight
    # Number of individuals in the front
    num_individuals = len(front)
    
    # Initialize crowding distances to zero
    distances = [0] * num_individuals
    
    # Sort by first objective (max_force)
    front_sorted_by_max_force = sorted(front, key=lambda x: x[1])

    print("DEBUG __", num_individuals, front_sorted_by_max_force, "\n\n", front)
    
    # Calculate crowding distance for max_force
    distances[0] = distances[-1] = float('inf')  # Boundary individuals have infinite crowding distance
    for i in range(1, num_individuals - 1):
        if front_sorted_by_max_force[-1][1] - front_sorted_by_max_force[0][1] == 0: ############ IF ALL VALUES ARE THE SAME
            distances[i] += 0
            continue

        distances[i] += (front_sorted_by_max_force[i + 1][1] - front_sorted_by_max_force[i - 1][1]) / \
                        (front_sorted_by_max_force[-1][1] - front_sorted_by_max_force[0][1])
    
    # Sort by second objective (weight)
    front_sorted_by_weight = front_sorted_by_max_force
    
    # Calculate crowding distance for weight
    for i in range(1, num_individuals - 1):
        if front_sorted_by_weight[-1][1] - front_sorted_by_weight[0][1] == 0:
            distances[i] += 0
            continue

        distances[i] += (front_sorted_by_weight[i + 1][2] - front_sorted_by_weight[i - 1][2]) / \
                        (front_sorted_by_weight[-1][2] - front_sorted_by_weight[0][2])
        
    return distances

    
    

    


### front format: [individual, max_force, weight]
def calc_fitness(population, max_force, weight):
    ## INITIATE ##
    indices = list(range(len(population)))
    individuals = list(zip(indices, max_force, weight))


    p_fronts = pareto_fronts(individuals)

    for front_index, front in enumerate(p_fronts, start=1): # FRONT IS SORTED BY INDEX AND NOT BY WEIGHT
        crowding_distance_values = crowding_distance(front)
        front = sorted(front, key=lambda x: x[1])  ################### SORTING FRONT BY MAX_FORCE!! #######################

        for i in range(len(front)):
            front_list = list(front[i]) # FIX
            if crowding_distance_values[i] == float('inf'):
                cd_distance = 3
            else:
                cd_distance = crowding_distance_values[i]

            local_fitness = 1 / ((front_index * 10) - cd_distance) # the hihger, the better
            # front[i].append(local_fitness)
            front_list.append(local_fitness) # FIX
            front[i] = tuple(front_list)  # Convert back to tuple after appending

        p_fronts[front_index - 1] = front  # Ensure p_fronts is updated with the modified front
    return p_fronts




def pareto_local_fitness(population, max_force, weight):
    failure_force = 1 / (1 + failure_force) # maximize failure_force
    pareto_fronts_ftns = calc_fitness(population, max_force, weight)

    flattened_pff = [item for sublist in pareto_fronts_ftns for item in sublist]
    # sorted_pff = sorted(flattened_pff, key=lambda x: x[0])
    # print("SORTED PF: ", sorted_pff)

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





### PASS FITNESS TO FITNESS.PY


def get_individual_to_vis(population, max_force, weight):
    # get first pareto_line
    pareto_fronts_ = calc_fitness(population, max_force, weight)
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


    # -> letzendlich brauche ich bloß den index von dem individual
    # damm kann ich im manager den rest requesten!
    return closest_index


population = [[1,2], [1,2], [1,2], [1,2], [1,2], [1,2], [1,2]] # population ist ja eigendlich bridge_nodes und bridge_connections
max_force = [11, 12, 13, 14, 15, 13, 0]
weight = [5, 0, 7, 2, 3, 4, 0]
indices = list(range(len(population)))
individuals = list(zip(indices, max_force, weight)) # index instead of population? -> then later combine all fronts and sort?
### FITNESS MUST BE IN SAME ORDER AS POPULATION ARRAY!!!
print("INDIVIDUAL TO VIS:", get_individual_to_vis(population, max_force, weight))
print("FITNES : : : : : : : ", pareto_local_fitness(population, max_force, weight))
print("PARETO FRONTS: ", calc_fitness(population, max_force, weight))

# not as many fitness as individuals in population!



   
### https://www.researchgate.net/publication/330704486_Search_Acceleration_of_Evolutionary_Multi-Objective_Optimization_Using_an_Estimated_Convergence_Point



