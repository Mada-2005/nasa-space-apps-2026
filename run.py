"""Task runner for the team (Windows, PowerShell).

Usage:
    python run.py setup      install Python packages
    python run.py fixtures   regenerate fake data in contracts/fixtures
    python run.py mock       API + app on fake data   -> http://localhost:8000
    python run.py api        API + app on real model output
    python run.py check      run all tests (do this before every push)
    python run.py train      train the model (lane A)
    python run.py predict    write ml/outputs/predictions.json (lane A)
"""
from __future__ import annotations

import os
import subprocess
import sys

PY = sys.executable


def sh(args: list[str], env_extra: dict | None = None) -> int:
    env = {**os.environ, **(env_extra or {})}
    print(">", " ".join(args))
    return subprocess.call(args, env=env)


COMMANDS = {
    "setup": lambda: sh([PY, "-m", "pip", "install", "-r", "requirements.txt"]),
    "fixtures": lambda: sh([PY, "ml/make_fixtures.py"]),
    "mock": lambda: sh([PY, "-m", "uvicorn", "api.main:app", "--reload", "--port", "8000"], {"MOCK": "1"}),
    "api": lambda: sh([PY, "-m", "uvicorn", "api.main:app", "--reload", "--port", "8000"], {"MOCK": "0"}),
    "check": lambda: sh([PY, "-m", "pytest", "-q"]),
    "train": lambda: sh([PY, "ml/train.py"]),
    "predict": lambda: sh([PY, "ml/predict.py"]),
}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(1)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    sys.exit(COMMANDS[sys.argv[1]]())
