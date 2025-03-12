FROM hashicorp/vault:latest

LABEL org.opencontainers.image.authors="Dima, Wolf, Jeremy"

RUN apk add --no-cache curl jq

ENV VAULT_ADDR="http://vault:8200"
ENV VAULT_API_ADDR="http://vault:8200"

RUN mkdir -p /vault/config /vault/data /vault/scripts /vault/policies /vault/certs && \
    chmod -R 770 /vault/data /vault/scripts /vault/certs

COPY conf/vault.hcl /vault/config/vault.hcl
COPY policies/* /vault/policies/
COPY tools/* /vault/scripts/

RUN chmod +x /vault/scripts/setup_vault.sh \
     /vault/scripts/unseal_and_login.sh \
     /vault/scripts/load_secrets.sh \
     /vault/scripts/setup_policies.sh \
     /vault/scripts/sync_certs.sh

EXPOSE 8200

CMD ["/bin/sh", "-c", "/vault/scripts/setup_vault.sh & vault server -config=/vault/config/vault.hcl"]
