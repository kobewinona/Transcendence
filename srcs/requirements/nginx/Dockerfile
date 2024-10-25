FROM debian:bookworm

# Set the metadata for the image an author
LABEL org.opencontainers.image.authors="Lera, Dima, Wolf, Jeremy"

# update, upgrade and install nginx
RUN apt-get update && apt-get upgrade -y &&\
	apt-get install -y nginx

# Clean the system and remove the cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# copy our configuration file of nginx to the container
COPY conf/nginx.conf /etc/nginx/nginx.conf

# Expose the port 443 for information
EXPOSE 443

# execute the command to start nginx
ENTRYPOINT [ "nginx", "-g", "daemon off;" ]
