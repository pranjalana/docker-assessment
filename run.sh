#!/bin/bash

echo "🏥 Starting Hospital Scheduler Container..."

# Run the container with port mapping
docker run -p 5000:5000 hospital-scheduler

echo "✅ Container is running!"
echo "🌐 Open: http://localhost:5000"
