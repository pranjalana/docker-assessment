# Use official nginx base image
FROM nginx:alpine

# Remove default nginx static files
RUN rm -rf /usr/share/nginx/html/*

# Copy static files to nginx directory
COPY static/ /usr/share/nginx/html/static/

# Create a simple health check page
RUN echo "<html><body><h1>Hospital Scheduler Static Content</h1><p>Static files are being served by nginx</p></body></html>" > /usr/share/nginx/html/index.html

# Copy custom nginx configuration (we'll create this next)
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 for HTTP
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]