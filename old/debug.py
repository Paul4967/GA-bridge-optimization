from PIL import Image, ImageDraw
import os

# Define the steps array
steps = [1, 2, 3, 4, 5, 9, 10, 12, 15, 17, 20, 31, 32, 45, 51, 52, 57, 98, 100, 104, 106, 116, 132, 139, 156, 157, 158, 165, 167, 171, 176, 240, 259, 272, 296, 301, 321, 334, 350, 437, 451, 457, 610, 681, 689, 694, 698, 742, 759, 779, 792, 822, 852, 894, 913, 949, 1020, 1029, 1046, 1049, 1061, 1121]

# Define image width
image_width = 1200

# Define line properties
line_color = "#ff642c"  # Orange
line_width = 4  # Pixels

import os
import re

# Define the folder containing the PNG files
output_folder = r"E:\_Projects\GA for generating optimal bridges\anderes\Simulation\bars"  # Change this to your folder path
os.makedirs(output_folder, exist_ok=True)

# Define image dimensions
image_width = 1200  # Fixed width
image_height = 800  # Fixed height

# Define line properties
line_color = "#ff642c"  # Orange
line_width = 10  # Pixels

# Define output folder
os.makedirs(output_folder, exist_ok=True)

# Generate images
for index, step in enumerate(steps, start=1):
    # Create a new white image (RGB mode)
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    # Ensure the step value does not exceed image width
    x_position = min(step, image_width - line_width)

    # Draw the vertical line at the given step position
    draw.line([(x_position, 0), (x_position, image_height)], fill=line_color, width=line_width)

    # Format filename with leading zeros (frame01, frame02, ..., frameXX)
    file_name = f"frame{index}.png"
    file_path = os.path.join(output_folder, file_name)

    # Save the image
    image.save(file_path)

    print(f"Saved: {file_path}")

print("Image generation complete!")
