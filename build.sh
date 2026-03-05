#!/bin/bash
set -e

echo "Current directory: $(pwd)"
echo "Listing files:"
ls -la

echo "Installing Python dependencies..."
if [ -f "backend/requirements.txt" ]; then
    pip install -r backend/requirements.txt
else
    echo "ERROR: backend/requirements.txt not found!"
    exit 1
fi

echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "Build complete!"
