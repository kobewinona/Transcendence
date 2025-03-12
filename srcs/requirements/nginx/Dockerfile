# Use the lightweight Alpine-based Nginx image
FROM nginx:alpine-slim

# Set metadata for the image (authors)
LABEL org.opencontainers.image.authors="Dima, Wolf, Jeremy"

# Ensure necessary directories exist and set proper permissions for the nginx user
RUN mkdir -p /tmp && chown -R nginx:nginx /tmp /var/cache/nginx /var/log/nginx

# Remove the default IPv6 configuration script to prevent unwanted modifications
RUN rm /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh

# Copy the custom Nginx configuration file into the container
COPY conf/nginx.conf /etc/nginx/nginx.conf

# Run the container as the non-root user 'nginx' for better security
USER nginx

# Expose port 8080 for internal access
EXPOSE 8080

# Start Nginx in the foreground (prevent daemonizing)
CMD ["nginx", "-g", "daemon off;"]