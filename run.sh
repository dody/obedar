#!/bin/bash

set -e

echo "=== $(date '+%Y-%m-%d %H:%M:%S') ==="

PROJECT_DIR="/home/jozef/pokus/obedar"

cd "$PROJECT_DIR"

# Update repository
git pull --ff-only

# Activate virtual environment and run Python script
source venv/bin/activate
python main.py
