#!/bin/bash
# this_file: scripts/release.sh
# Release script for twardown-py

set -e

echo "🚀 Preparing release for twardown-py..."

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

# Check if version is provided
if [ -z "$1" ]; then
    print_error "Usage: $0 <version>"
    print_error "Example: $0 1.0.0"
    exit 1
fi

VERSION=$1

# Validate version format (basic semver check)
if [[ ! $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+(\.[0-9]+)?)?$ ]]; then
    print_error "Invalid version format. Use semantic versioning (e.g., 1.0.0 or 1.0.0-alpha.1)"
    exit 1
fi

# Check if working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    print_error "Working directory is not clean. Please commit all changes first."
    exit 1
fi

# Check if we're on the right branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    print_warning "You are not on the main branch (currently on: $CURRENT_BRANCH)"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if tag already exists
if git rev-parse "v$VERSION" >/dev/null 2>&1; then
    print_error "Tag v$VERSION already exists!"
    exit 1
fi

# Run full build process
print_status "Running full build process..."
./scripts/build.sh

# Update CHANGELOG.md
print_status "Updating CHANGELOG.md..."
if [ ! -f "CHANGELOG.md" ]; then
    echo "# Changelog" > CHANGELOG.md
    echo "" >> CHANGELOG.md
fi

# Add new release entry to changelog
TODAY=$(date +%Y-%m-%d)
TEMP_FILE=$(mktemp)
echo "## [$VERSION] - $TODAY" > "$TEMP_FILE"
echo "" >> "$TEMP_FILE"
echo "### Added" >> "$TEMP_FILE"
echo "- Release v$VERSION" >> "$TEMP_FILE"
echo "" >> "$TEMP_FILE"
cat CHANGELOG.md >> "$TEMP_FILE"
mv "$TEMP_FILE" CHANGELOG.md

# Commit changelog update
git add CHANGELOG.md
git commit -m "Update CHANGELOG.md for v$VERSION"

# Create and push tag
print_status "Creating and pushing tag v$VERSION..."
git tag -a "v$VERSION" -m "Release v$VERSION"
git push origin "v$VERSION"

# Push the changelog commit
git push origin "$CURRENT_BRANCH"

print_status "Release v$VERSION created successfully! 🎉"
print_status "The CI/CD pipeline will now build and publish the release."
print_status "Check the GitHub Actions for progress: https://github.com/twardoch/twardown-py/actions"