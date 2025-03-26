#!/bin/sh

VAULT_ADDR="http://vault:8200"
SSL_DIR="/vault-init/ssl"
POSTGRES_ENV_FILE="/vault-init/postgres/.env.db"
API_ENV_FILE="/vault-init/api/.env.key"
GRAFANA_ENV_FILE="/vault-init/grafana/.env.grafana"
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
  echo "⚠️ Postgres .env.db file not found at $POSTGRES_ENV_FILE"
else
  echo "📄 Reading $POSTGRES_ENV_FILE..."
  vault kv put secret/postgres \
    $(grep -v '^#' "$POSTGRES_ENV_FILE" | xargs)
  echo "✅ Postgres secrets stored in Vault!"
fi

# Add backend API keys to Vault
echo "🔑 Storing Backend API keys from $API_ENV_FILE into Vault..."

if [ ! -f "$API_ENV_FILE" ]; then
  echo "❌ ERROR: API env file not found at $API_ENV_FILE"
else
  echo "📄 Reading $API_ENV_FILE..."
  vault kv put secret/backend \
    $(grep -v '^#' "$API_ENV_FILE" | xargs)
    
  if [ $? -eq 0 ]; then
    echo "✅ Backend API secrets stored in Vault!"
  else
    echo "❌ ERROR: Failed to store backend API secrets!" >&2
  fi
fi

# Add Grafana admin credentials to Vault
echo "🔑 Storing Grafana admin credentials from $GRAFANA_ENV_FILE into Vault..."

if [ ! -f "$GRAFANA_ENV_FILE" ]; then
  echo "❌ ERROR: Grafana env file not found at $GRAFANA_ENV_FILE"
else
  echo "📄 Reading $GRAFANA_ENV_FILE..."
  vault kv put secret/grafana \
    $(grep -v '^#' "$GRAFANA_ENV_FILE" | xargs)
    
  if [ $? -eq 0 ]; then
    echo "✅ Grafana admin secrets stored in Vault!"
  else
    echo "❌ ERROR: Failed to store Grafana secrets!" >&2
  fi
fi


echo "✅ All SSL secrets have been stored in Vault!"
exit 0
