#!/bin/sh

VAULT_ADDR="http://vault:8200"
UNSEAL_KEYS_FILE="/vault-init/unseal/unseal_keys.txt"
ROOT_TOKEN_FILE="/vault-init/unseal/root_token.txt"

echo "🔄 Waiting for Vault to start..."
while true; do
  RESPONSE=$(curl -ks $VAULT_ADDR/v1/sys/health || echo "error")
  if echo "$RESPONSE" | grep -q '"initialized":'; then
    echo "✅ Vault is available."
    break
  fi
  echo "⏳ Vault isn't ready yet..."
  sleep 2
done


echo "🔄 Checking Vault status..."
INIT_STATUS=$(curl -ks $VAULT_ADDR/v1/sys/health | jq -r '.initialized')

if [ "$INIT_STATUS" = "false" ]; then
    echo "🚀 Initialising Vault..."
    vault operator init -format=json > /vault-init/unseal/init.json

    jq -r '.unseal_keys_b64[]' /vault-init/unseal/init.json > $UNSEAL_KEYS_FILE
    jq -r '.root_token' /vault-init/unseal/init.json > $ROOT_TOKEN_FILE
    echo "Vault root token: $(cat /vault-init/unseal/root_token.txt)"

    echo "✅ Vault is initialized and stored."
fi

echo "🔓 Unsealing Vault..."
for key in $(head -n 3 $UNSEAL_KEYS_FILE); do
  vault operator unseal $key
done


echo "🔧 Running setup_policies.sh..."
sh /vault-init/setup_policies.sh

echo "🔧 Running store_secrets.sh..."
sh /vault-init/setup_secrets.sh


echo "✅ Vault-init setup completed. Keeping container alive..."
tail -f /dev/null

echo "✅ Vault is unsealed!"
exit 0

