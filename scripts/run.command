#!/bin/zsh
set -e

# ...existing code...

# move to project root (handles spaces in path)
cd "$(dirname "$0")/.."

# If virtualenv doesn't exist, create it and install requirements
if [ ! -d "env" ]; then
  echo "Virtualenv 'env' not found — creating..."
  python3 -m venv "env"
  source "env/bin/activate"
  if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r "requirements.txt"
  else
    echo "requirements.txt not found — skipping pip install."
  fi
else
  source "env/bin/activate"
fi

python3 main.py

# ...existing code...