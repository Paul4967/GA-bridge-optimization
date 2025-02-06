import json
import sys
import os

# Get the absolute path to the project folder
project_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_folder)
data_folder = os.path.join(project_folder, 'data')


file_path_termination = os.path.join(data_folder, 'final_solutions.json')

open(file_path_termination, "w").close()

