#!/bin/bash

echo "🔨 Building Hospital Scheduler Docker image..."

# Build the Docker image
docker build -t hospital-scheduler .

echo "✅ Build complete!"
echo "📦 Image built: hospital-scheduler"
echo "🚀 To run: docker run -p 5000:5000 hospital-scheduler"
