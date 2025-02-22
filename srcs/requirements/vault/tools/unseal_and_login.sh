#!/bin/sh

set -e

VAULT_ADDR="http://0.0.0.0:8200"
VAULT_UNSEAL_FILE="/vault/data/unseal_keys.json"
VAULT_TOKEN_FILE="/vault/data/root_token"

# echo "🔓 Unsealing Vault..."
if vault status 2>/dev/null | grep -q "Sealed.*true"; then
    while IFS= read -r key; do
        vault operator unseal "$key"
    done < "$VAULT_UNSEAL_FILE"
fi

echo "🔑 Logging in with root token..."
vault login $(cat "$VAULT_TOKEN_FILE") > /dev/null 2>&1

echo "🔄 Checking if KV secrets engine is already enabled..."
if ! vault secrets list | grep -q "^secret/"; then
    echo "🔄 Enabling KV secrets engine..."
    vault secrets enable -path=secret kv
else
    echo "✅ KV engine already enabled."
fi
