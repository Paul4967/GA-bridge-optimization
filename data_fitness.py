import numpy as np
import matplotlib.pyplot as plt

# The fitness data
fitness = [5, 30, 27, 19, 9, 7, 17, 1, 17, 29, 3, 9, 15, 20, 19, 11, 16,
           3, 3, 8, 16, 12, 10, 13, 9, 12, 4, 27, 27, 5, 25, 17, 6, 30,
           12, 26, 10, 4, 20, 24, 9, 5, 4, 14, 24, 8, 6, 8, 15, 29, 8,
           17, 1, 5, 6, 13, 10, 18, 13, 14, 19, 20, 18, 16, 5, 8, 7, 18,
           10, 2, 4, 1, 27, 26, 15, 14, 23, 4, 17, 7, 2, 1, 13, 8, 10,
           29, 2, 20, 23, 15, 14, 15, 15, 25, 3, 2, 8, 26, 16, 14]

# Reshape the data into a 10x10 grid
fitness_grid = np.array(fitness).reshape(10, 10)

# Calculate the variance of the data
variance = np.var(fitness)

# Create the heatmap
plt.figure(figsize=(6, 6))
plt.imshow(fitness_grid, cmap='inferno', interpolation='nearest')
plt.colorbar(label='Fitness Value')

# Add axis labels, title, and variance information
plt.title(f'Population Fitness Heatmap (Variance = {variance:.2f})')

# Display the plot
plt.show()
