import matplotlib.pyplot as plt

# Given data
pareto_fronts = [
    [(0, 11, 5, 0.14285714285714285), (5, 13, 4, 0.125), (3, 14, 2, 0.14285714285714285)],
    [(2, 13, 7, 0.058823529411764705), (4, 150, 3, 0.058823529411764705)]
]

# Initialize the plot
plt.figure(figsize=(10, 6))

# Loop through each Pareto front and plot the points
for front_index, front in enumerate(pareto_fronts):
    x_values = [point[1] for point in front]  # Extract x-coordinates
    y_values = [point[2] for point in front]  # Extract y-coordinates

    # Plot the points and connect them with lines
    plt.plot(x_values, y_values, marker='o', label=f'Pareto Front {front_index + 1}')

# Adjust the scale to fit the data
plt.autoscale()

# Add labels, legend, and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Pareto Fronts')
plt.legend()

# Add grid
plt.grid(True)

# Show the plot
plt.show()
