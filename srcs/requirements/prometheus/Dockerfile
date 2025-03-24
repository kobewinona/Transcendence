FROM prom/prometheus

LABEL org.opencontainers.image.authors="Dima, Wolf, Jeremy"

COPY /conf/prometheus.yml /etc/prometheus/prometheus.yml
COPY /conf/alert.rules.yml /etc/prometheus/alert.rules.yml

EXPOSE 9090

