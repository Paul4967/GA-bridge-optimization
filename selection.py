# tournament selection:
# https://ijcseonline.org/pdf_paper_view.php?paper_id=5522&3-IJCSE-08999.pdf
# only calculate fitness for k individuals -> save computation power --> NO! store fitness together with model and id

# for each parent that should reproduce, a turnament is run (i think)
# or 1 tournament and select e.g. 50 best percent

import random



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



