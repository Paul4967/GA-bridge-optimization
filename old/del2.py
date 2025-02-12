import os
import re

# Define the folder containing the PNG files
folder_path = r"E:\_Projects\GA for generating optimal bridges\anderes\Simulation\steps_2"  # Change this to your folder path


# Get all PNG files matching the pattern "generation_step_<number>.png"
png_files = [f for f in os.listdir(folder_path) if re.match(r"generation_step_\d+\.png", f)]

# Extract the numerical part and sort by it
png_files.sort(key=lambda x: int(re.search(r"\d+", x).group()))

# Rename files with sequential numbers
for index, file_name in enumerate(png_files, start=1):
    old_path = os.path.join(folder_path, file_name)
    new_path = os.path.join(folder_path, f"frame{index}.png")

    # Rename the file
    os.rename(old_path, new_path)

print(f"Renamed {len(png_files)} PNG files in {folder_path}")
