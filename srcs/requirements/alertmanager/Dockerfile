FROM prom/alertmanager

LABEL org.opencontainers.image.authors="Dima, Wolf, Jeremy"

COPY /conf/config.yml /etc/alertmanager/config.yml

EXPOSE 9093

CMD ["--config.file=/etc/alertmanager/config.yml"]