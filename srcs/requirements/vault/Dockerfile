# Step 1 : Use the official Vault image
FROM hashicorp/vault:latest

# Step 2 : Install curl and jq (needed for scripts)
RUN apk add --no-cache curl jq

# Step 3 : Define environment variables
ENV VAULT_ADDR="http://vault:8200"
ENV VAULT_API_ADDR="http://vault:8200"

# Step 4 : Create necessary directories
RUN mkdir -p /vault/config /vault/data /vault/scripts /vault/policies /vault/certs && \
    chmod -R 770 /vault/data /vault/scripts /vault/certs

# Step 5 : Copy the Vault configuration file, scripts and policies
COPY conf/vault.hcl /vault/config/vault.hcl
COPY policies/* /vault/policies/
COPY tools/* /vault/scripts/

# Step 6 : Give execution permissions to scripts
RUN chmod +x /vault/scripts/setup_vault.sh \
     /vault/scripts/unseal_and_login.sh \
     /vault/scripts/load_secrets.sh \
     /vault/scripts/setup_policies.sh \
     /vault/scripts/sync_certs.sh

# Step 7 : Start Vault and load secrets on startup
EXPOSE 8200
CMD ["/bin/sh", "-c", "/vault/scripts/setup_vault.sh & vault server -config=/vault/config/vault.hcl"]
