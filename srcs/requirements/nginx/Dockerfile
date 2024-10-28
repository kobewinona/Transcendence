FROM nginx:stable-alpine

# Set the metadata for the image an author
LABEL org.opencontainers.image.authors="Lera, Dima, Wolf, Jeremy"

# copy our configuration file of nginx to the container
COPY conf/nginx.conf /etc/nginx/nginx.conf

# Expose the port 443 for information
EXPOSE 443

# execute the command to start nginx
ENTRYPOINT [ "nginx", "-g", "daemon off;" ]
