#!/bin/bash
# this_file: scripts/quality.sh
# Code quality check script for twardown-py

set -e

echo "🔍 Checking code quality for twardown-py..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    print_warning "Virtual environment not found. Creating one..."
    python3 -m venv .venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
print_status "Installing dependencies..."
pip install -e ".[dev]"

# Run linting
print_status "Running linting with Ruff..."
python -m ruff check src tests

# Run formatting check
print_status "Checking code formatting with Ruff..."
python -m ruff format --check src tests

# Run type checking
print_status "Running type checking with mypy..."
python -m mypy src

print_status "Code quality checks completed successfully! ✨"