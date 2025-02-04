import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.colors import LinearSegmentedColormap, Normalize, TwoSlopeNorm
import matplotlib.patches as mpatches

# Your data
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
            469.965, -165.0008, -304.9642, 901.2222, 637.2603,
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
            [4.0, 5.1], [6.0, 5.1], [1.1, 3.1], [3.1, 5.1], 
            [0.0, 2.0], [2.0, 4.0], [4.0, 6.0]
        ],
        "forces": [
            469.965, -5165.0008, -304.9642, 201.2222, 637.2603,
            -806.0777, -749.8622, -3304.9642, 469.965, -5165.0008, -304.9642
        ]
    }
]




import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize

import matplotlib.patches as mpatches

step = 2
# Access the correct dictionary in the data list by matching the step value
step_data = next(item for item in data if item["step"] == step)

# Extract the relevant information
bridge_nodes = step_data["bridge_nodes"]
bridge_connections = step_data["bridge_connections"]
forces = step_data["forces"]


# 3. Create a mapping from node IDs to their indices in bridge_nodes
id_to_index = {node[0]: idx for idx, node in enumerate(bridge_nodes)}

# 4. Normalize the forces for color mapping
force_min, force_max = min(forces), max(forces)
norm = Normalize(vmin=force_min, vmax=force_max)

# 5. Define a custom colormap (green -> blue -> yellow)
colors = [(0, 0.8, 1), (0, 0.85, 0), (1, 0.7, 0)] # Green -> Blue -> Yellow # RGB/255
cmap = LinearSegmentedColormap.from_list("ForceMap", colors)

# 6. Plotting function
def plot_bridge_with_forces(nodes, connections, forces):
    nodes = np.array(nodes)
    plt.figure(figsize=(8, 6))  # Adjust figure size to accommodate color bar
    
    # Plot the nodes (as points)
    plt.scatter(nodes[:, 1], nodes[:, 2], color='red', label='Nodes', zorder=5)
    
    # Plot the connections (as lines) with color coding for forces
    for i, connection in enumerate(connections):
        node1_id, node2_id = connection
        if node1_id in id_to_index and node2_id in id_to_index:
            node1_idx = id_to_index[node1_id]
            node2_idx = id_to_index[node2_id]
            color = cmap(norm(forces[i]))  # Get color based on force
            x_coords = [nodes[node1_idx, 1], nodes[node2_idx, 1]]
            y_coords = [nodes[node1_idx, 2], nodes[node2_idx, 2]]
            
            # Draw the line
            plt.plot(x_coords, y_coords, color=color, linewidth=2, zorder=2)
            
            # Add force label at the midpoint of the connection
            mid_x = (x_coords[0] + x_coords[1]) / 2
            mid_y = (y_coords[0] + y_coords[1]) / 2
            plt.text(mid_x, mid_y, f"{forces[i]:.1f}", color='black', 
                    fontsize=10, ha='center', va='center', zorder=10)
    
    # Label the nodes
    for idx, node in enumerate(nodes):
        plt.text(node[1] + 0.1, node[2] + 0.1, str(int(node[0])), fontsize=12, zorder=10)
    
    plt.xlim(-1, 7)
    plt.ylim(-1, 4)

    # Ensure equal scaling of both axes
    plt.gca().set_aspect('equal', adjustable='box')
    
    # Adding grid and labels
    plt.grid(True)
    plt.xlabel("X-axis (meter)", fontsize=12)
    plt.ylabel("Y-axis (meter)", fontsize=12)
    plt.title("Bridge Visualization with Forces")

    # Create custom legend entries for force and compression
    neutral_patch = mpatches.Patch(color=cmap(norm(0)), label='None (Neutral Force)', linewidth=2)
    compression_patch = mpatches.Patch(color=cmap(norm(min(forces))), label='Compression (Negative Force)', linewidth=2)
    tension_patch = mpatches.Patch(color=cmap(norm(max(forces))), label='Tension (Positive Force)', linewidth=2)

    # Add legend
    plt.legend(handles=[neutral_patch, compression_patch, tension_patch], loc='upper right', fontsize=10)

    # Add a color bar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array(forces)  # Set the range of forces
    cbar = plt.colorbar(sm, ax=plt.gca(), fraction=0.03, pad=0.04)
    cbar.set_label("Force (N)", fontsize=12)  # Add label with units
    cbar.ax.tick_params(labelsize=10)  # Adjust tick size

    

# 7. Plot the bridge with forces and log the image
plot_bridge_with_forces(bridge_nodes, bridge_connections, forces)
plt.tight_layout()
plt.show()





