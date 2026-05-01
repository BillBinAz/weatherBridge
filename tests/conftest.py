import sys
import os

# Add the src directory to the path so tests can import modules
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, os.path.abspath(src_path))

