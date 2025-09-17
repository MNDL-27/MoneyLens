FROM nginx:alpine

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Create simple error pages
RUN echo '<h1>404 Not Found</h1>' > /usr/share/nginx/html/404.html
RUN echo '<h1>50x Server Error</h1>' > /usr/share/nginx/html/50x.html

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]