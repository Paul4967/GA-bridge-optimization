# tournament selection:
# https://ijcseonline.org/pdf_paper_view.php?paper_id=5522&3-IJCSE-08999.pdf
# only calculate fitness for k individuals -> save computation power --> NO! store fitness together with model and id

# for each parent that should reproduce, a turnament is run (i think)
# or 1 tournament and select e.g. 50 best percent

import random
import numpy as np


def tournament_selection(population, fitnesses, k, num_selections): # k = tournament size
    selected = []
    for _ in range(num_selections):
        tournament = random.sample(range(len(population)), k)
        winner = max(tournament, key=lambda i: fitnesses[i])
        selected.append(population[winner])
    return selected



"""
def tournament_selection(population, fitnesses, k, num_selections):
    selected = []
    selected_indices = set()  # Track already selected individuals

    while len(selected) < num_selections and len(selected_indices) < len(population):
        tournament = random.sample([i for i in range(len(population)) if i not in selected_indices], k)
        winner = max(tournament, key=lambda i: fitnesses[i])
        selected.append(population[winner])
        selected_indices.add(winner)  # Prevent re-selection

    return selected
"""


def select_PT(population_RT, population_RT_fitness, POPULATION_SIZE):
    # Sort indices based on fitness in ascending order
    sorted_indices = np.argsort(population_RT_fitness)

    # Select the top half with the greatest fitness
    top_half_indices = sorted_indices[-(POPULATION_SIZE // 2):]

    # Get the corresponding individuals and their fitness values
    population_PT = [population_RT[i] for i in top_half_indices]
    population_PT_fitness = [population_RT_fitness[i] for i in top_half_indices]


    return population_PT, population_PT_fitness




def crowded_tournament_selection(population, fitnesses, k, num_selections): # k = tournament size
    selected = []
    selected_indices = set()  # Track already selected individuals
    while len(selected) < num_selections and len(selected_indices) < len(population):
        tournament = random.sample([i for i in range(len(population)) if i not in selected_indices], k)
        winner = max(tournament, key=lambda i: fitnesses[i])
        selected.append(population[winner])
        selected_indices.add(winner)  # Prevent re-selection
    return selected









def select_PT_tournament(population_RT, population_RT_fitness, tournament_size, num_selections):
    selected_population = []
    selected_fitness = []
    
    for _ in range(num_selections):
        # Randomly select 'tournament_size' individuals
        tournament_indices = random.sample(range(len(population_RT)), tournament_size)
        
        # Find the best individual in the tournament (lowest fitness if minimizing, highest if maximizing)
        best_index = max(tournament_indices, key=lambda i: population_RT_fitness[i])
        
        # Add the best individual to the selected population
        selected_population.append(population_RT[best_index])
        selected_fitness.append(population_RT_fitness[best_index])
    
    return selected_population, selected_fitness