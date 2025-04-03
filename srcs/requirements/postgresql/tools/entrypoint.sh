#!/bin/sh

ENV_FILE="/run/secrets/postgres_env/.env.db"
SOURCE_FILE="/run/secrets/postgres_env/init-users.sql"
TARGET_FILE="/docker-entrypoint-initdb.d/init-users.sql"

echo "⏳ Waiting for Vault Agent to generate .env.db..."
while [ ! -f "$ENV_FILE" ]; do
  sleep 1
done

echo "✅ .env.db found. Loading secrets into environment..."
set -a
. "$ENV_FILE"
set +a

echo "⏳ Waiting for Vault Agent to generate init-users.sql ..."
while [ ! -f "$SOURCE_FILE" ]; do
  sleep 1
done

echo "✅ SQL init found, starting PostgreSQL..."
cp "$SOURCE_FILE" "$TARGET_FILE"
chmod 644 "$TARGET_FILE"

echo "🚀 Starting PostgreSQL with environment from Vault"
exec docker-entrypoint.sh postgres
