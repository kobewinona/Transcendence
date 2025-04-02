FROM hashicorp/vault:1.19.0

LABEL org.opencontainers.image.authors="Dima, Wolf, Jeremy"

COPY conf/ /vault/config/

RUN mkdir -p /vault/certs /vault/postgres /vault/backend /vault/grafana /vault/postgres_backend && \
    chmod -R 777 /vault/certs && \
    chown -R vault:vault /vault/certs /vault/postgres /vault/backend /vault/grafana /vault/postgres_backend && \
    chmod -R 755 /vault/certs /vault/grafana /vault/postgres && \
    chmod -R 750 /vault/backend /vault/postgres_backend 

EXPOSE 8201

CMD ["vault", "agent", "-config=/vault/config/vault-agent.hcl"]
