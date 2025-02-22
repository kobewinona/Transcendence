#!/bin/sh

set -e  # Stop on error

VAULT_ADDR="http://0.0.0.0:8200"
VAULT_UNSEAL_FILE="/vault/data/unseal_keys.json"
VAULT_TOKEN_FILE="/vault/data/root_token"
INIT_FILE="/tmp/vault_init.json"
MAX_RETRIES=5
RETRY_INTERVAL=3
COUNTER=0

echo "🔄 Waiting for Vault to be ready..."
while ! curl -s "$VAULT_ADDR/v1/sys/seal-status" > /dev/null; do
    if [ "$COUNTER" -ge "$MAX_RETRIES" ]; then
        echo "❌ Vault isn't accessible after $MAX_RETRIES tries."
        exit 1
    fi
    echo "⏳ Vault is not ready yet... retrying in $RETRY_INTERVAL seconds."
    sleep "$RETRY_INTERVAL"
    COUNTER=$((COUNTER+1))
done
echo "✅ Vault is up and running!"


echo "🔄 Checking Vault status..."
if vault status 2>/dev/null | grep -q "Initialized.*true"; then
    echo "✅ Vault is already initialized."
else
    echo "🚀 Initializing Vault..."
    vault operator init -format=json > "$INIT_FILE"
    if [ ! -s "$INIT_FILE" ]; then
        echo "❌ Error: Vault initialization failed!"
        exit 1
    fi
    echo "💾 Saving Root Token..."
    cat "$INIT_FILE" | jq -r ".root_token" | tee "$VAULT_TOKEN_FILE" > /vault/secrets/root_token
    echo "🔑 Storing Unseal Keys..."
    cat "$INIT_FILE" | jq -r '.unseal_keys_b64 | join("\n")' "$INIT_FILE" > "$VAULT_UNSEAL_FILE"
    echo "🗑️ Cleaning temporary files..."
    rm -f "$INIT_FILE"

    if [ ! -f "$VAULT_TOKEN_FILE" ] || [ ! -f "$VAULT_UNSEAL_FILE" ]; then
    echo "❌ Error: storage of root token and unseal keys failed !"
        exit 1
    fi
fi


# Can be modify to use an external service has AWS
echo "🔓 Unsealing Vault..."
/bin/sh /vault/scripts/unseal_and_login.sh

# Load the secret
echo "🔐 Loading Secrets..."
/bin/sh /vault/scripts/load_secrets.sh

# Transfer ssl certificat to Nginx shared volume
echo "📤 Transferring SSL certificates to shared volume..."
/bin/sh /vault/scripts/sync_certs.sh

# echo "🔑 Applying policies..."
# /bin/sh /vault/scripts/setup_policies.sh

echo "✅ Vault is ready!"
