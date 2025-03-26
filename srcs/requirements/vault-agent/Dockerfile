FROM hashicorp/vault:1.19.0

LABEL org.opencontainers.image.authors="Dima, Wolf, Jeremy"

COPY conf/ /vault/config/

RUN mkdir -p /vault/certs /vault/postgres /vault/backend /vault/grafana && \
    chmod -R 777 /vault/certs && \
    chown -R vault:vault /vault/certs /vault/postgres /vault/backend /vault/grafana&& \
    chmod -R 755 /vault/certs /vault/grafana  && \
    chmod -R 750 /vault/postgres /vault/backend 

EXPOSE 8201

CMD ["vault", "agent", "-config=/vault/config/vault-agent.hcl"]
