# BASE IMAGE & AUTHOR INFORMATION
FROM postgres:16

LABEL org.opencontainers.image.authors="Dima, Wolf, Jeremy"

COPY tools/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 5432

ENTRYPOINT ["/entrypoint.sh"]
