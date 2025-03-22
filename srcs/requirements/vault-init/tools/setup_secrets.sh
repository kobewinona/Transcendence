#!/bin/sh

VAULT_ADDR="http://vault:8200"
SSL_DIR="/vault-init/ssl"
POSTGRES_ENV_FILE="/vault-init/postgres/.env"
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


# Add ssl certificat secret to vault
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

# Add postgres access admin to vault
echo "🔑 Storing Postgres credentials in Vault..."

if [ ! -f "$POSTGRES_ENV_FILE" ]; then
  echo "⚠️ Postgres .env file not found at $POSTGRES_ENV_FILE"
else
  echo "📄 Reading $POSTGRES_ENV_FILE..."
  vault kv put secret/postgres \
    $(grep -v '^#' "$POSTGRES_ENV_FILE" | xargs)
  echo "✅ Postgres secrets stored in Vault!"
fi


echo "✅ All SSL secrets have been stored in Vault!"
exit 0
