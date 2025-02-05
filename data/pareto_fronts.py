import json
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.cm as cm  # For colormap
import math

file_path = os.path.join(os.path.dirname(__file__), "pareto_fronts.json")

# Load Pareto fronts from JSON
json_file = file_path
with open(json_file, "r") as f:
    data = json.load(f)

steps = sorted(map(int, data.keys()))  # Get available steps
current_step = steps[0]  # Default to first step


def plot_pareto(step):
    """Plots all Pareto fronts for the selected step with magma colormap."""
    # Convert slider value to integer (handling the float value)
    step = int(float(step))
    
    ax.clear()
    ax.set_xlabel("Failure Force")
    ax.set_ylabel("Weight")
    ax.set_title(f"Pareto Fronts - Population at Step {math.ceil(step / 2)}")

    # Use the 'magma' colormap
    colormap = cm.magma  # Magma colormap
    fronts = data[str(step)]  # Retrieve fronts for the selected step

    # Normalize the number of fronts to the colormap
    num_fronts = len(fronts)
    colors = [colormap(i / num_fronts) for i in range(num_fronts)]  # Get color for each front

    for i, front in enumerate(fronts):
        front = sorted(front, key=lambda x: x[0])  # Sort by failure force
        failure_forces, weights = zip(*front)
        ax.plot(failure_forces, weights, marker='o', linestyle='-', 
                color=colors[i], label=f'Front {i+1}')
    
    ax.legend()
    ax.grid()
    canvas.draw()


# Create Tkinter window
root = tk.Tk()
root.title("Pareto Front Viewer")

# Create a Matplotlib figure
fig, ax = plt.subplots(figsize=(10, 8))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Create a slider to select step (population)
slider = ttk.Scale(root, from_=steps[0], to=steps[-1], orient="horizontal", command=plot_pareto)
slider.pack(fill="x", padx=10, pady=10)
slider.set(current_step)  # Set default position

# Initial plot
plot_pareto(current_step)

# Run Tkinter loop
root.mainloop()