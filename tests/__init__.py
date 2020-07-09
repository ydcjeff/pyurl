"""Testing init."""

import os
from pathlib import Path

FILE = os.path.join(str(Path.home()), ".pyurl/pyurl.db")
if os.path.exists(FILE):
    print(f"==> Found db at {FILE}")
