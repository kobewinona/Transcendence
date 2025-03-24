#!/bin/sh

ENV_FILE="/run/secrets/postgres_env/.env.db"

echo "⏳ Waiting for Vault Agent to generate .env..."
while [ ! -f "$ENV_FILE" ]; do
  sleep 1
done

echo "✅ .env found. Loading into environment..."
set -a
. "$ENV_FILE"
set +a

exec docker-entrypoint.sh postgres
