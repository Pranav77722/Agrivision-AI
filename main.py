import sys
from pathlib import Path

# Add backend to Python path so app.* modules resolve cleanly
root_dir = Path(__file__).resolve().parent
backend_dir = str(root_dir / "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.main import app

