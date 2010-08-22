# hack around with the python path for the examples.
import sys
from os import path

env_root = path.dirname(path.join(path.abspath(__file__)))
sys.path.insert(0, env_root)
sys.path.insert(0, path.join(env_root, '..'))
