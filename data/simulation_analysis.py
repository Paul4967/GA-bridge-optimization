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
from math import log10, floor, isinf, isnan


# READ DATA
file_path = os.path.join(os.path.dirname(__file__), "evolution_data.json")
try:
    with open(file_path, 'r') as f:
            data = json.load(f)
except FileNotFoundError:
    print(f"Error: {file_path} does not exist.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")

# Create a custom colormap with white at zero
colors = [
    (0.0, "#4093FF"),   # Minimum (e.g., negative forces)
    (0.5, "#4A4A4A"),  # Midpoint (zero)
    (1.0, "#FF7C2C")     # Maximum (positive forces)
]
custom_cmap = LinearSegmentedColormap.from_list("CustomMap", colors)

def norm_width(failure_force, forces):
    f_force = abs(failure_force)
    max_force = max(abs(f) for f in forces if not (f == float('inf') or f == float('-inf')))
    if f_force != float('inf') and f_force != float('-inf'):
        normalized_width = f_force / max_force
        width = round(2 + normalized_width * 8)
    else:
        width = 10
    return width


# Plotting function
def plot_bridge_with_forces(nodes, connections, forces, weight, failure_force, step):
    plt.close('all')  # Close all existing figures
    fig, ax = plt.subplots(figsize=(10, 8))  # Create figure and axis explicitly

    ## ERROR PREVENTION----------------
    finite_forces = [f for f in forces if not isinf(f)]  # Filter out infinite values
    min_force = min(finite_forces)
    max_force = max(finite_forces)
    
    # Ensure vmin, vcenter, vmax are in ascending order
    if min_force > 0:
        vcenter = min_force + 0.00001
    elif max_force < 0:
        vcenter = max_force - 0.00001
    else:
        vcenter = 0
    ####-------------------------------
    
    # Create a normalization where zero is exactly in the center
    #norm = TwoSlopeNorm(vmin=min(forces), vcenter=0, vmax=max(forces))
    print("TSN", min_force, vcenter, max_force)
    norm = TwoSlopeNorm(vmin=min_force, vcenter=vcenter, vmax=max_force)
    
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
            # Assign purple for infinite forces, otherwise use the colormap
            if isinf(forces[i]):
                color = '#80F21B'  # Purple for infinite forces
            else:
                #color = custom_cmap(norm(forces[i]))  # Get color based on force
                if forces[i] <= 0:
                    color = '#0E9BFF'
                else:
                    color = '#FF642C'

            x_coords = [nodes[node1_idx][1], nodes[node2_idx][1]]
            y_coords = [nodes[node1_idx][2], nodes[node2_idx][2]]
            
            # Draw the line
            ax.plot(x_coords, y_coords, color=color, linewidth=norm_width(forces[i], forces), zorder=2)
            
            # Add force label at the midpoint of the connection
            def format_force(f):
                if isnan(f) or isinf(f):  
                    return "inf" if f > 0 else "-inf"  # Handle infinite values
                if f == 0:
                    return "0"
                exponent = floor(log10(abs(f)))
                base = f / (10 ** exponent)
                return f"{base:.2f}e{exponent}" if exponent != 0 else f"{base:.2f}"

            # Add force label at the midpoint of the connection
            mid_x = (x_coords[0] + x_coords[1]) / 2
            mid_y = (y_coords[0] + y_coords[1]) / 2
            formatted_force = format_force(forces[i])
            ax.text(mid_x, mid_y, formatted_force, color='black', 
                    fontsize=10, ha='center', va='center', zorder=10,
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))
    
    # Label the nodes
    # for idx, node in enumerate(nodes):
        # ax.text(node[1] + 0.1, node[2] + 0.1, f"({node[1]:.1f}, {node[2]:.1f})", 
            # fontsize=7, zorder=10)
    
    
    ax.set_xlim(-1, 25)
    ax.set_ylim(-1, 9)

    # Ensure equal scaling of both axes
    ax.set_aspect('equal', adjustable='box')
    
    # Adding grid and labels
    ax.grid(True)

    # Set the grid ticks to 1 by 1
    ax.set_xticks(range(-1, 26, 1))  # Grid markings on x-axis from -1 to 25 with a step of 1
    ax.set_yticks(range(-1, 10, 1))  # Grid markings on y-axis from -1 to 11 with a step of 1
    # Ensure equal scaling of both axes
    
    ax.set_xlabel("Length in m", fontsize=12)
    ax.set_ylabel("Height in m", fontsize=12)
    fig.suptitle(f'Generation: {step}', fontsize=16, fontweight='bold', x=0.1, y=0.9, ha='left')
    ax.set_title(f'weight: {weight:.2f}kg    failure_force: {abs(failure_force):.2f}N')
    

    # Create custom legend entries for force and compression
    # neutral_patch = mpatches.Patch(color=custom_cmap(norm(0)), label='Low failure force', linewidth=2)
    inf_patch = mpatches.Patch(color='#80F21B', label='Infinite failure force (0 Load)', linewidth=2)
    compression_patch = mpatches.Patch(color=custom_cmap(norm(min(forces))), label='Compression', linewidth=2)
    tension_patch = mpatches.Patch(color=custom_cmap(norm(max(forces))), label='Tension', linewidth=2)

    # Add legend
    ax.legend(handles=[inf_patch, compression_patch, tension_patch], loc='upper right', fontsize=10)

    # COLORBAR
    """sm = plt.cm.ScalarMappable(cmap=custom_cmap, norm=norm)
    sm.set_array([])  # Set an empty array to avoid errors
    cbar = fig.colorbar(sm, ax=ax)
    cbar.set_label('failure force in N', fontsize=12)
    """

    


    ### SAVE AS IMG ###
    # Define the folder path
    folder_path = r"E:\_Projects\GA for generating optimal bridges\anderes\Simulation\steps"  # Change this to your desired folder

    # Ensure the directory exists
    os.makedirs(folder_path, exist_ok=True)

    # Dynamically generate the filename
    file_name = f"generation_step_{step}.png"
    file_path = os.path.join(folder_path, file_name)

    # Save the figure
    plt.savefig(file_path, dpi=300, bbox_inches='tight')


    return fig, ax





def update_plot(step):
    global canvas
    step_data = next((item for item in data if item["step"] == step), None)
    if step_data is None:
        print(f"No data for step {step}")
        return

    # Scale the forces and node positions
    forces = [force for force in step_data["failure_forces"]]  # Scale forces by 10
    nodes = [[node[0], node[1] / 10, node[2] / 10] for node in step_data["all_nodes"]]  # Scale coordinates
    connections = step_data["all_connections"]
    weight = step_data["weight"]
    failure_force = step_data["min_failure_force"]
    
    fig, ax = plot_bridge_with_forces(nodes, connections, forces, weight, failure_force, step)
    
    if canvas:
        for widget in root.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)



def save_to_img():
    for item in data:
        step =  item["step"]
        update_plot(step)
save_to_img()


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