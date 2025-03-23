FROM hashicorp/vault:1.19.0

LABEL org.opencontainers.image.authors="Dima, Wolf, Jeremy"

COPY conf/vault-agent.hcl /vault/config/vault-agent.hcl

RUN mkdir -p /vault/certs /vault/postgres /vault/backend && \
    chmod -R 777 /vault/certs && \
    chown -R vault:vault /vault/certs /vault/postgres /vault/backend && \
    chmod -R 755 /vault/certs  && \
    chmod -R 750 /vault/postgres /vault/backend

EXPOSE 8201

CMD ["vault", "agent", "-config=/vault/config/vault-agent.hcl"]
