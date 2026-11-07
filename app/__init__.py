import sys
from pathlib import Path

# Add backend directory to sys.path
_root = Path(__file__).resolve().parent.parent
_backend = _root / "backend"
if str(_backend) not in sys.path:
    sys.path.insert(0, str(_backend))

# Delegate all app.* package lookups to backend/app
_real_app = _backend / "app"
__path__.clear()
__path__.append(str(_real_app))
