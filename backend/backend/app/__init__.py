import sys
from pathlib import Path

_backend = Path(__file__).resolve().parents[2]
if str(_backend) not in sys.path:
    sys.path.insert(0, str(_backend))

_real_app = _backend / "app"
__path__.clear()
__path__.append(str(_real_app))
