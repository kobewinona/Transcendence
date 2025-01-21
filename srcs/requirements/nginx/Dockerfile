FROM nginx:stable

LABEL org.opencontainers.image.authors="Lera, Dima, Wolf, Jeremy"

COPY conf/nginx.conf /etc/nginx/nginx.conf

RUN chmod 644 /etc/nginx/nginx.conf && chown root:root /etc/nginx/nginx.conf

EXPOSE 80 443

ENTRYPOINT [ "nginx", "-g", "daemon off;" ]
