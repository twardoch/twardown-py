#!/bin/bash
# this_file: scripts/test.sh
# Test script for twardown-py

set -e

echo "🧪 Testing twardown-py..."

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

# Run tests with coverage
print_status "Running tests with coverage..."
python -m pytest tests/ -v --cov=twardown_py --cov-report=term-missing --cov-report=xml --cov-report=html

# Show coverage summary
print_status "Coverage report generated in htmlcov/index.html"

print_status "Testing completed successfully! ✅"