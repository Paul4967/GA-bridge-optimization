import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm, LinearSegmentedColormap

# Data (as per your provided structure)
data = [
    {
        "step": 1,
        "bridge_nodes": [
            [0.0, 0, 0], [2.0, 2, 0], [4.0, 4, 0], [6.0, 6, 0],
            [1.2, 1, 2], [2.1, 2, 1], [5.2, 5, 2]
        ],
        "bridge_connections": [
            [0.0, 1.2], [1.2, 2.1], [2.1, 2.0], [2.1, 4.0],
            [1.2, 5.2], [5.2, 4.0], [5.2, 6.0]
        ],
        "forces": [
            1469.965, -165.0008, -304.9642, 901.2222, 637.2603,
            -806.0777, -749.8622
        ]
    },
    {
        "step": 2,
        "bridge_nodes": [
            [0.0, 0, 0], [2.0, 2, 0], [4.0, 4, 0], [6.0, 6, 0],
            [1.1, 1, 1], [3.1, 3, 1], [5.1, 5, 1]
        ],
        "bridge_connections": [
            [0.0, 1.1], [2.0, 1.1], [2.0, 3.1], [4.0, 3.1],
            [4.0, 5.1], [6.0, 5.1], [1.1, 3.1], [3.1, 5.1]
        ],
        "forces": [
            469.965, -2165.0008, -304.9642, 201.2222, 637.2603,
            -806.0777, -749.8622, -3304.9642
        ]
    }
]

# Step to visualize
step = 1
# Access the correct dictionary in the data list by matching the step value
step_data = next(item for item in data if item["step"] == step)

# Extract the forces and corresponding node positions (only x, y)
forces = step_data["forces"]
nodes = step_data["bridge_nodes"]
positions = np.array([node[:2] for node in nodes])  # Take only x and y for 2D plot

# Define a custom colormap with white at zero
colors = [
    (0.0, "blue"),   # Minimum (e.g., -80)
    (0.5, "white"),  # Midpoint (zero)
    (1.0, "red")     # Maximum (e.g., +20)
]
custom_cmap = LinearSegmentedColormap.from_list("CustomMap", colors)

# Create a normalization where zero is exactly in the center
norm = TwoSlopeNorm(vmin=min(forces), vcenter=0, vmax=max(forces))

# Create a scatter plot
plt.figure(figsize=(8, 6))
scatter = plt.scatter(positions[:, 0], positions[:, 1], c=forces, cmap=custom_cmap, norm=norm, s=100)

# Add colorbar
cbar = plt.colorbar(scatter)
cbar.set_label('Force (units)')

# Add labels and title
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title(f'Forces Visualization at Step {step}')

# Show plot
plt.show()
