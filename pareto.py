
################
population = [1, 2, 3, 4, 5]
max_force = [11, 12, 13, 14, 15]
weight = [9, 8, 7, 6, 5]

################
# pipulation: bridge_nodes, bridge_connections

# for each individual:
# 1: jedes individuum plotten
def calc_pareto_fitness(max_force, weight, population):
    
    while len(population) is not 0:
        pareto_front = [] # each front needs other name (i)
    
        new_population = []
        for i, individual in enumerate(population):
            new_population.append([individual, weight[i], max_force[i]])
            # individual = [bridge_nodes, bridge_connections]

        print("P: ", new_population)
        front_line_index = 1
        for individual in new_population[:]:

            _, individual_weight, individual_max_force = individual
            
            if min(max_force) > individual_weight and min(weight) > individual_max_force:
                # individual i is not dominated!
                pareto_front.append(individual)
                new_population.remove(individual)
        


        # SORT PARETO FRON (left to right -> weight)
        front_sorted = sorted(pareto_front, key=lambda x: x[max_force])

        # Calculate crowdingDistance ### -1 to acces last one
        for i, individual in enumerate(front_sorted):
            if i-1 != 0 and i+1 != len(front_sorted):
                crowding_distance = ((front_sorted[i+1][1] - front_sorted[i-1][1]) / (front_sorted[-1][1] - front_sorted[0][1])) + ((front_sorted[i+1][2] - front_sorted[i-1][2]) / (front_sorted[-1][2] - front_sorted[0][2]))
            else:
                fitness = front_line_index * 1
                # (lowest fitness) -> the lower, the better
                continue

        # normalize crowding_distance
        






calc_pareto_fitness(max_force, weight, population)




### https://www.researchgate.net/publication/330704486_Search_Acceleration_of_Evolutionary_Multi-Objective_Optimization_Using_an_Estimated_Convergence_Point