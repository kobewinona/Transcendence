#!/bin/sh

VAULT_ADDR="http://vault:8200"
SSL_DIR="/vault-init/ssl"
VAULT_TOKEN_FILE="/vault-init/unseal/vault-init-token.txt"


if [ ! -f "$VAULT_TOKEN_FILE" ]; then
  echo "❌ ERROR: Vault token file not found!"
  exit 1
fi

VAULT_TOKEN=$(cat "$VAULT_TOKEN_FILE")
export VAULT_TOKEN="$VAULT_TOKEN"

if [ -z "$VAULT_TOKEN" ]; then
  echo "❌ ERROR: Vault token is empty!"
  exit 1
fi

echo "✅ Vault token successfully loaded!"


echo "🔑 Storing SSL secrets in Vault..."

if [ ! -d "$SSL_DIR" ]; then
  echo "⚠️ SSL directory $SSL_DIR not found. Skipping..."
  exit 1
fi

if ! vault secrets list | grep -q "^secret/"; then
    vault secrets enable -path=secret kv-v2
else
    echo "ℹ️ Secrets engine 'kv' already enabled."
fi


for cert_file in "$SSL_DIR"/*; do
  filename=$(basename "$cert_file")
  
  if vault kv put secret/ssl/"$filename" content="$(cat "$cert_file")"; then
    echo "✅ $filename stocké avec succès dans Vault!"
  else
    echo "❌ ERROR: Unable to store $filename in Vault!" >&2
  fi
done


echo "✅ All SSL secrets have been stored in Vault!"
exit 0
