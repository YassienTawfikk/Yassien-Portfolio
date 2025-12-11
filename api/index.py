import os
import sys

# Get the directory of this script (api/index.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
# The project root is one level up from 'api'
root_dir = os.path.dirname(current_dir)

# CRITICAL: Add the root directory to Python's path so 'app' and 'utils' can be imported
sys.path.append(root_dir)

# CRITICAL: Change the working directory to the project root.
# This makes file paths like "data/*.json" resolve correctly.
os.chdir(root_dir)

# Import the main application server
from app import server as app