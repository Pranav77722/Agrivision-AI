import sys
from pathlib import Path

# Ensure parent directory (backend/) is in python path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app.main import app
