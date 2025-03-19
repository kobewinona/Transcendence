FROM hashicorp/vault:1.19.0

LABEL org.opencontainers.image.authors="Dima, Wolf, Jeremy"

RUN apk add --no-cache jq curl

RUN mkdir -p /vault/certs

COPY /tools/bootstrap.sh /vault-init/bootstrap.sh
COPY /tools/setup_policies.sh /vault-init/setup_policies.sh
COPY /tools/setup_secrets.sh /vault-init/setup_secrets.sh

RUN chmod +x /vault-init/*.sh

ENTRYPOINT ["/bin/sh", "/vault-init/bootstrap.sh"]