import json
import matplotlib.pyplot as plt
import os

# READ DATA
file_path = os.path.join(os.path.dirname(__file__), "first_pareto_fronts.json")
try:
    with open(file_path, 'r') as f:
        pareto_fronts = json.load(f)
except FileNotFoundError:
    print(f"Error: {file_path} does not exist.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")

# Organize the data by steps
pareto_dict = {}
for entry in pareto_fronts:
    step = entry['step']
    pareto_dict[step] = entry['pareto_front']

# Get sorted step keys
sorted_steps = sorted(pareto_dict.keys(), key=int)

# Generate colors from the cool colormap
num_fronts = len(sorted_steps)
colors = [plt.cm.cool(i / (num_fronts - 1)) for i in range(num_fronts)]

# Plot each front
plt.figure(figsize=(8, 6))

for step, color in zip(sorted_steps, colors):
    pareto_data = pareto_dict[step]
    weights = [point[0] for point in pareto_data]
    failure_forces = [point[1] for point in pareto_data]

    plt.scatter(weights, failure_forces, color=color, label=f"Pareto Front {step}", edgecolors="black")
    plt.plot(weights, failure_forces, linestyle="--", color=color, alpha=0.7)

# Labels and title
plt.xlabel("Weight")
plt.ylabel("Failure Force")
plt.title("Multiple Pareto Fronts (Cool Colormap)")
plt.legend()
plt.grid(True)

# Auto-scaling
plt.autoscale()

# Show plot
plt.show()
