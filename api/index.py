import os
import sys

# 1. Determine the root folder (one level up from 'api')
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. Add root to the system path (so we can import 'app.py')
sys.path.append(root_dir)

# 3. CRITICAL: Change the working directory to root
# This ensures that open("data/file.json") finds the file!
os.chdir(root_dir)

# 4. Import the server
from app import server as app