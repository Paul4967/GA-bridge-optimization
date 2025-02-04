### DEPENDENCIES ### ----------------------

import sys
import os

# Get the absolute path to the project folder
project_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(project_folder)
import json
import math
import initialization_reworked as initialization
#import mutation_reworked as mutation
import m_r as mutation
import time
import copy
import crossover
import ga_modules
import pareto_reworked as pareto
import importlib
import fitness_reworked as ftns
import selection
import numpy as np
import torch
import tensorflow as tf
from torch.utils.tensorboard import SummaryWriter

# -----------------------------------------