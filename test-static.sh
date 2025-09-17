#!/bin/bash

# Local Static Site Testing Script
# Usage: ./test-static.sh

set -e

echo "🧪 Testing static site locally..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Check if deployment directory exists
if [ ! -d "static-site-deploy" ]; then
    print_status "No deployment directory found. Running build first..."
    ./build-static.sh
fi

# Check if serve is installed globally
if ! command -v serve &> /dev/null; then
    print_status "Installing 'serve' package globally..."
    npm install -g serve
fi

print_status "Starting local server for static site..."
print_success "Static site will be available at: http://localhost:5000"
print_status "Press Ctrl+C to stop the server"

# Serve the static files
cd static-site-deploy
serve -p 5000 .