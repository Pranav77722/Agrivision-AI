import sys
from pathlib import Path

# Ensure both 'app.*' and 'backend.app.*' work regardless of execution directory
_backend_dir = Path(__file__).resolve().parent.parent
_parent_dir = _backend_dir.parent

for _p in [str(_backend_dir), str(_parent_dir)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

if "app" in sys.modules and "backend.app" not in sys.modules:
    sys.modules["backend.app"] = sys.modules["app"]
