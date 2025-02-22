#!/bin/sh

set -e  # Stop on error if any command fails

VAULT_ADDR="http://0.0.0.0:8200"
VAULT_TOKEN=$(cat /vault/data/root_token)

echo "🔐 Loading secrets from Docker Secrets..."

# Read the JSON file and insert each secret into Vault
jq -c '.secrets[]' /run/secrets/vault_secrets_json | while read -r secret; do
    path=$(echo "$secret" | jq -r '.path')

    echo "📝 Storing secret at path: $path"

    # Read the data and construct the command with key/value pairs
    data=$(echo "$secret" | jq -r '.data | to_entries | map("\(.key)=\(.value|@sh)") | join(" ")')

    if [ -z "$data" ]; then
        echo "⚠️ No valid data for $path, skipping..."
        continue
    fi

    # Properly construct the Vault command
    cmd="vault kv put $path $data"

    # Execute the Vault command
    sh -c "$cmd"

    echo "✅ Stored secret at $path"
done

echo "✅ Secrets successfully loaded into Vault."
