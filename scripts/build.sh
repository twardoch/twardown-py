#!/bin/bash
# this_file: scripts/build.sh
# Build script for twardown-py

set -e

echo "🔨 Building twardown-py..."

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

# Clean previous builds
print_status "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/ .pytest_cache/

# Run tests
print_status "Running tests..."
python -m pytest tests/ -v --cov=twardown_py --cov-report=term-missing --cov-report=xml --cov-fail-under=90

# Run code quality checks
print_status "Running code quality checks..."
python -m ruff check src tests
python -m mypy src

# Build package
print_status "Building package..."
python -m build

# Validate package
print_status "Validating package..."
python -m twine check dist/*

# Show version
print_status "Package version:"
python -c "from twardown_py import __version__; print(__version__)"

print_status "Build completed successfully! 🎉"
print_status "Built artifacts are in the 'dist/' directory"