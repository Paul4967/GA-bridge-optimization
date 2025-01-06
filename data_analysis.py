import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import TwoSlopeNorm, LinearSegmentedColormap
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json
import os


# READ DATA
file_path = 'evolution_data.json'
with open(file_path, 'r') as f:
        data = json.load(f)

# Create a custom colormap with white at zero
colors = [
    (0.0, "#177fff"),   # Minimum (e.g., negative forces)
    (0.5, "#17e800"),  # Midpoint (zero)
    (1.0, "#ff5b24")     # Maximum (positive forces)
]
custom_cmap = LinearSegmentedColormap.from_list("CustomMap", colors)

# Plotting function
def plot_bridge_with_forces(nodes, connections, forces):
    plt.close('all')  # Close all existing figures
    fig, ax = plt.subplots(figsize=(8, 6))  # Create figure and axis explicitly

    ## ERROR PREVENTION----------------
    min_force = min(forces)
    max_force = max(forces)
    
    # Ensure vmin, vcenter, vmax are in ascending order
    if min_force == max_force:
        # If all forces are the same, set a valid range
        min_force = -1  # Use a small negative value for compression
        max_force = 1   # Use a small positive value for tension
        vcenter = 0
    else:
        vcenter = 0
    ####-------------------------------
    
    # Create a normalization where zero is exactly in the center
    #norm = TwoSlopeNorm(vmin=min(forces), vcenter=0, vmax=max(forces))
    norm = TwoSlopeNorm(vmin=min_force, vcenter=0.000000000001, vmax=max_force)
    
    # Mapping node IDs to index positions in the nodes array
    id_to_index = {node[0]: idx for idx, node in enumerate(nodes)}
    
    # Plot the nodes (as points)
    ax.scatter(np.array(nodes)[:, 1], np.array(nodes)[:, 2], color='red', label='Nodes', zorder=5)
    
    # Plot the connections (as lines) with color coding for forces
    for i, connection in enumerate(connections):
        node1_id, node2_id = connection
        if node1_id in id_to_index and node2_id in id_to_index:
            node1_idx = id_to_index[node1_id]
            node2_idx = id_to_index[node2_id]
            color = custom_cmap(norm(forces[i]))  # Get color based on force
            x_coords = [nodes[node1_idx][1], nodes[node2_idx][1]]
            y_coords = [nodes[node1_idx][2], nodes[node2_idx][2]]
            
            # Draw the line
            ax.plot(x_coords, y_coords, color=color, linewidth=2, zorder=2)
            
            # Add force label at the midpoint of the connection
            mid_x = (x_coords[0] + x_coords[1]) / 2
            mid_y = (y_coords[0] + y_coords[1]) / 2
            ax.text(mid_x, mid_y, f"{forces[i]:.1f}", color='black', 
                    fontsize=10, ha='center', va='center', zorder=10,
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))
    
    # Label the nodes
    for idx, node in enumerate(nodes):
        ax.text(node[1] + 0.1, node[2] + 0.1, str(int(node[0])), fontsize=12, zorder=10)
    
    ax.set_xlim(-1, 7)
    ax.set_ylim(-1, 4)

    # Ensure equal scaling of both axes
    ax.set_aspect('equal', adjustable='box')
    
    # Adding grid and labels
    ax.grid(True)
    ax.set_xlabel("Length in m", fontsize=12)
    ax.set_ylabel("Height in m", fontsize=12)
    ax.set_title("Bridge Visualization with Forces")

    # Create custom legend entries for force and compression
    neutral_patch = mpatches.Patch(color=custom_cmap(norm(0)), label='None (Neutral Force)', linewidth=2)
    compression_patch = mpatches.Patch(color=custom_cmap(norm(min(forces))), label='Compression (Negative Force)', linewidth=2)
    tension_patch = mpatches.Patch(color=custom_cmap(norm(max(forces))), label='Tension (Positive Force)', linewidth=2)

    # Add legend
    ax.legend(handles=[neutral_patch, compression_patch, tension_patch], loc='upper right', fontsize=10)

    # COLORBAR
    sm = plt.cm.ScalarMappable(cmap=custom_cmap, norm=norm)
    sm.set_array([])  # Set an empty array to avoid errors
    cbar = fig.colorbar(sm, ax=ax)
    cbar.set_label('Force in N')

    return fig, ax

def update_plot(step):
    global canvas
    step_data = next((item for item in data if item["step"] == step), None)
    if step_data is None:
        print(f"No data for step {step}")
        return

    forces = step_data["forces"]
    nodes = step_data["all_nodes"]
    connections = step_data["all_connections"]
    
    fig, ax = plot_bridge_with_forces(nodes, connections, forces)
    
    if canvas:
        for widget in root.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)






root = tk.Tk()
root.title("Bridge Visualization")

canvas = None

control_frame = tk.Frame(root)
control_frame.pack(side=tk.TOP, fill=tk.X)

# Create a label for the slider
slider_label = tk.Label(control_frame, text="Step:")
slider_label.pack(side=tk.LEFT)

# Create an IntVar to store the current step
current_step = tk.IntVar(value=1)

# Create the slider with integer steps
step_slider = ttk.Scale(control_frame, from_=1, to=100, orient=tk.HORIZONTAL, length=600, 
                        variable=current_step, command=lambda s: current_step.set(round(float(s))))
step_slider.pack(side=tk.LEFT, padx=10)

# Create a label to display the current step
step_value_label = tk.Label(control_frame, textvariable=current_step)
step_value_label.pack(side=tk.LEFT)

def slider_changed(event):
    step = current_step.get()
    update_plot(step)

step_slider.bind("<ButtonRelease-1>", slider_changed)

# Update the step value label in real-time
def update_step_label(event):
    current_step.set(round(float(step_slider.get())))

step_slider.bind("<Motion>", update_step_label)

update_plot(1)  # Start with Step 1







## INSERT ##
current_displayed_step = None
previous_step = 0

def check_for_updates():
    global current_displayed_step, data, previous_step

    # Read the latest JSON data
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                new_data = json.load(f)
            except json.JSONDecodeError:
                print("Error reading JSON data")
                root.after(1000, check_for_updates)  # Retry after 1 second
                return
    else:
        print("JSON file not found.")
        root.after(1000, check_for_updates)  # Retry after 1 second
        return

    # Update global data and find the latest step
    data = new_data
    latest_step = max(item["step"] for item in data)

    # Check if a new step has been added
    if latest_step > previous_step:
        # Update slider range dynamically
        step_slider.config(to=latest_step)

        # Jump to the latest step (move slider to the right)
        current_step.set(latest_step)
        update_plot(latest_step)

        # Update the previous_step tracker
        previous_step = latest_step

    # Schedule the next check after 1 second, but only if a new step has not been added
    root.after(1000, check_for_updates)  # Check every 1 second, but only react to changes


check_for_updates()
## INSERT END ##









root.mainloop()




# CALL JSON DATA AND FETCH HIGHEST STEP, THEN CALL update_plot(step)