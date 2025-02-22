#!/bin/sh

set -e  # Stop on error

VAULT_ADDR="http://0.0.0.0:8200"
VAULT_TOKEN=$(cat /vault/token/nginx/token.txt)
CERT_PATH="secret/nginx_ssl"
DEST_PATH="/vault/certs"

echo "🔐 Fetching SSL certificates from Vault..."

# Check if the directory exists
mkdir -p $DEST_PATH

# Retrieve certificates from Vault
SSL_CERT=$(vault kv get -field=ssl_cert $CERT_PATH)
SSL_KEY=$(vault kv get -field=ssl_key $CERT_PATH)

if [ -z "$SSL_CERT" ] || [ -z "$SSL_KEY" ]; then
    echo "❌ Error: Could not retrieve certificates from Vault!"
    exit 1
fi

# Write certificates to the shared volume
echo "$SSL_CERT" > $DEST_PATH/nginx.crt
echo "$SSL_KEY" > $DEST_PATH/nginx.key

echo "✅ Certificates successfully copied to $DEST_PATH"
