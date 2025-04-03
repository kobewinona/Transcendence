#!/bin/sh

VAULT_ADDR="http://vault:8200"
VAULT_TOKEN_FILE="/vault-init/unseal/root_token.txt"

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


echo "🔑 Applying Vault policies..."

if [ -z "$VAULT_TOKEN" ]; then
  echo "❌ ERROR: VAULT_TOKEN is empty. Check root_token.txt!"
  exit 1
fi

if ! vault auth list | grep -q "approle/"; then
  echo "🔄 Enabling AppRole authentication..."
  vault auth enable approle
else
  echo "✅ AppRole authentication already enabled."
fi


vault policy write vault-init-policy - <<EOF
path "sys/mounts" {
  capabilities = ["read", "list", "update"]
}

path "sys/mounts/kv" {
  capabilities = ["create", "update"]
}

path "sys/mounts/secret" {
  capabilities = ["create", "update", "read", "list", "delete"]
}

path "kv/*" {
  capabilities = ["create", "update", "read", "list"]
}

path "kv/data/ssl/*" {
  capabilities = ["create", "update", "read", "list"]
}

path "secret/*" {
  capabilities = ["create", "update", "read", "list"]
}

path "secret/data/ssl/*" {
  capabilities = ["create", "update", "read", "list"]
}
EOF

vault policy write vault-agent-auth - <<EOF
path "auth/approle/role/vault-agent-role/role-id" {
  capabilities = ["read"]
}
EOF


vault policy write vault-agent-policy - <<EOF
path "secret/data/ssl/*" {
  capabilities = ["read", "list"]
}

path "secret/metadata/ssl/*" {
  capabilities = ["list"]
}

path "secret/data/postgres/admin" {
  capabilities = ["read"]
}

path "secret/metadata/postgres/admin" {
  capabilities = ["list"]
}

path "secret/data/postgres/backend" {
  capabilities = ["read"]
}

path "secret/metadata/postgres/backend" {
  capabilities = ["list"]
}

path "secret/data/postgres/exporter" {
  capabilities = ["read"]
}

path "secret/metadata/postgres/exporter" {
  capabilities = ["list"]
}

path "secret/data/backend" {
  capabilities = ["read"]
}

path "secret/metadata/backend" {
  capabilities = ["list"]
}

path "secret/data/grafana" {
  capabilities = ["read"]
}

path "secret/metadata/grafana" {
  capabilities = ["list"]
}
EOF


echo "🔄 Creating AppRole vault-agent-role..."
if ! vault read auth/approle/role/vault-agent-role 2>/dev/null; then
  vault write auth/approle/role/vault-agent-role token_policies="vault-agent-auth, vault-agent-policy"
else
  echo "✅ AppRole vault-agent-role already exists."
fi


vault read auth/approle/role/vault-agent-role/role-id -format=json | jq -r ".data.role_id" > /vault/auth/role_id
vault write -f auth/approle/role/vault-agent-role/secret-id -format=json | jq -r ".data.secret_id" > /vault/auth/secret_id

echo "🔄 Creating Vault-Init token..."
VAULT_TOKEN_FILE="/vault-init/unseal/vault-init-token.txt"

VAULT_INIT_TOKEN=$(vault token create -policy=vault-init-policy -format=json | jq -r ".auth.client_token")

if [ -z "$VAULT_INIT_TOKEN" ]; then
  echo "❌ ERROR: Failed to create Vault-Init token!"
  exit 1
fi

echo "$VAULT_INIT_TOKEN" > "$VAULT_TOKEN_FILE"

echo "✅ Vault-Init token successfully created and stored!"


echo "✅ Vault policies applied!"
