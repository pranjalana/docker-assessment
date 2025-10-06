#!/bin/bash

echo "🔨 Building nginx static content image..."

# Build the nginx Docker image
docker build -f nginx.Dockerfile -t hospital-scheduler-nginx .

echo "✅ nginx build complete!"
echo "📦 Image built: hospital-scheduler-nginx"
echo "🚀 To run: docker run -p 8080:80 hospital-scheduler-nginx"