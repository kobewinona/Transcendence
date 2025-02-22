#!/bin/sh

set -e  # Stop on error

VAULT_ADDR="http://0.0.0.0:8200"
VAULT_TOKEN=$(cat /vault/data/root_token)

echo "🔑 Nginx policy..."
vault policy write nginx-policy /vault/policies/nginx-policy.hcl

echo "✅ Policies applied!"

echo "🔑 Generating tokens..."

mkdir -p /vault/token/nginx

# Create tokens with specific policies
NGINX_TOKEN=$(vault token create -policy=nginx-policy -format=json | jq -r ".auth.client_token")

# Store tokens for services
echo "$NGINX_TOKEN" > /vault/token/nginx/token.txt

echo "✅ Tokens generated and stored!"