#!/bin/sh

VAULT_ADDR="http://vault:8200"
SSL_DIR="/vault-init/ssl"
POSTGRES_ENV_FILE="/vault-init/postgres/.env.db"
POSTGRES_BACKEND="/vault-init/postgres/.env.backend"
POSTGRES_EXPORTER="/vault-init/postgres/.env.exporter"
API_ENV_FILE="/vault-init/api/.env.key"
GRAFANA_ENV_FILE="/vault-init/grafana/.env.grafana"
VAULT_TOKEN_FILE="/vault-init/unseal/vault-init-token.txt"


if [ ! -f "$VAULT_TOKEN_FILE" ]; then
  echo "❌ ERROR: Vault token file not found!"
  exit 1
fi

VAULT_TOKEN=$(cat "$VAULT_TOKEN_FILE")
export VAULT_TOKEN="$VAULT_TOKEN"


update_secret_if_changed() {
  secret_path="$1"
  file_path="$2"

  if [ ! -f "$file_path" ]; then
    echo "❌ File not found: $file_path"
    return 1
  fi

  local_value=$(cat "$file_path")
  remote_value=$(vault kv get -field=content "$secret_path" 2>/dev/null)

  if [ "$local_value" != "$remote_value" ]; then
    echo "🔄 Update of $secret_path in Vault"
    vault kv put "$secret_path" content="$local_value"
  else
    echo "✅ Nothing change for $secret_path"
  fi
}

update_kv_secret_if_changed() {
  secret_path="$1"
  env_file="$2"

  if [ ! -f "$env_file" ]; then
    echo "❌ File not found: $env_file"
    return 1
  fi

  remote_data=$(vault kv get -format=json "$secret_path" 2>/dev/null | jq -r '.data.data')

  changed=0
  while IFS='=' read -r key value; do
    [ -z "$key" ] && continue
    current_val=$(echo "$remote_data" | jq -r --arg k "$key" '.[$k]')
    if [ "$value" != "$current_val" ]; then
      changed=1
      break
    fi
  done < <(grep -v '^#' "$env_file")

  if [ "$changed" -eq 1 ]; then
    echo "🔄 Update of $secret_path in Vault"
    vault kv put "$secret_path" $(grep -v '^#' "$env_file" | xargs)
  else
    echo "✅ Nothing change for $secret_path"
  fi
}


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

current_type=$(vault secrets list -format=json | jq -r '."secret/".options.version')

if [ "$current_type" != "2" ]; then
  echo "⚠️ Vault 'secret/' mount is not kv-v2. Reconfiguring..."
  vault secrets disable secret/
  vault secrets enable -path=secret kv-v2
else
  echo "ℹ️ Secrets engine 'secret/' is already kv-v2"
fi

for cert_file in "$SSL_DIR"/*; do
  filename=$(basename "$cert_file")
  update_secret_if_changed "secret/ssl/$filename" "$cert_file"
done


# Add postgres access admin to vault
echo "🔑 Storing Postgres credentials in Vault..."

if [ ! -f "$POSTGRES_ENV_FILE" ]; then
  echo "⚠️ Postgres .env.db file not found at $POSTGRES_ENV_FILE"
else
  echo "📄 Reading $POSTGRES_ENV_FILE..."
  update_kv_secret_if_changed secret/postgres/admin "$POSTGRES_ENV_FILE"

  echo "✅ Postgres secrets stored in Vault!"
fi

echo "🔑 Storing Postgres backend credentials in Vault..."

if [ ! -f "$POSTGRES_BACKEND" ]; then
  echo "⚠️ Postgres .env.backend file not found at $POSTGRES_BACKEND"
else
  echo "📄 Reading $POSTGRES_BACKEND..."
  update_kv_secret_if_changed secret/postgres/backend "$POSTGRES_BACKEND"

  echo "✅ Postgres backend secrets stored in Vault!"
fi

echo "🔑 Storing Postgres exporter credentials in Vault..."

if [ ! -f "$POSTGRES_EXPORTER" ]; then
  echo "⚠️ Postgres .env.exporter file not found at $POSTGRES_EXPORTER"
else
  echo "📄 Reading $POSTGRES_EXPORTER..."
  update_kv_secret_if_changed secret/postgres/exporter "$POSTGRES_EXPORTER"

  echo "✅ Postgres exporter secrets stored in Vault!"
fi

# Add backend API keys to Vault
echo "🔑 Storing Backend API keys from $API_ENV_FILE into Vault..."

if [ ! -f "$API_ENV_FILE" ]; then
  echo "❌ ERROR: API env file not found at $API_ENV_FILE"
else
  echo "📄 Reading $API_ENV_FILE..."
  update_kv_secret_if_changed secret/backend "$API_ENV_FILE"

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
  update_kv_secret_if_changed secret/grafana "$GRAFANA_ENV_FILE"

  if [ $? -eq 0 ]; then
    echo "✅ Grafana admin secrets stored in Vault!"
  else
    echo "❌ ERROR: Failed to store Grafana secrets!" >&2
  fi
fi


echo "✅ All SSL secrets have been stored in Vault!"
exit 0
