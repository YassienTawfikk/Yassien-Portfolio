import os
import sys

# Add the parent directory to the system path to find app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import server as app
