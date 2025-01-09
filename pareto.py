


# for each individual:
# 1: jedes individuum plotten
def calc_pareto_fitness(max_force, weight, population):
    
    while len(population) is not 0:
        pareto_front = [] # each front needs other name (i)
    
        for i, individual in enumerate(population):
            individual_weight = weight[i]
            individual_max_force = max_force[i]

            # CALCULATE FIRST PARETO FRONT #
            # if there is an individual with lower weight AND lower cost, individual[i] is dominated! -> dont add! -> if nothing better: add to front1 ->

            if min(max_force) > individual_weight and min(weight) > individual_max_force:
                # individual i is not dominated!
                pareto_front.append(individual[i])
        
        # subtract pareto front from population




### https://www.researchgate.net/publication/330704486_Search_Acceleration_of_Evolutionary_Multi-Objective_Optimization_Using_an_Estimated_Convergence_Point