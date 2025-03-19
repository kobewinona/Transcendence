FROM hashicorp/vault:1.19.0

LABEL org.opencontainers.image.authors="Dima, Wolf, Jeremy"

RUN apk add --no-cache curl jq && \
    mkdir -p /vault/config /vault/data /vault/policies /vault/certs && \
    chmod -R 770 /vault/data /vault/policies && \
    chown -R vault:vault /vault

COPY conf/vault.hcl /vault/config/vault.hcl

USER vault

EXPOSE 8200

ENTRYPOINT ["vault", "server", "-config=/vault/config/vault.hcl"]
