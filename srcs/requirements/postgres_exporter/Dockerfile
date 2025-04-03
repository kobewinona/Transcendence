FROM quay.io/prometheuscommunity/postgres-exporter:latest

LABEL org.opencontainers.image.authors="Dima, Wolf, Jeremy"

COPY tools/wait-for-env.sh /usr/local/bin/wait-for-env.sh

USER 100:1000

ENTRYPOINT ["/usr/local/bin/wait-for-env.sh"]
