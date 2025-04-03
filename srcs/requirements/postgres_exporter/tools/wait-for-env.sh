#!/bin/sh

ENV_FILE="/run/secrets/postgres_exporter/.env.exporter"

echo "⏳ Waiting for Vault Agent to generate $ENV_FILE..."
while [ ! -f "$ENV_FILE" ]; do
  sleep 1
done

echo "✅ Found environment file. Sourcing..."
set -a
. "$ENV_FILE"
set +a

DATA_SOURCE_NAME="postgresql://${EXPORTER_USER}:${EXPORTER_PASSWORD}@postgres:5432/${POSTGRES_DB}?sslmode=disable"

export PG_EXPORTER_DISABLE_SETTINGS_METRICS=false
export PG_EXPORTER_DISABLE_DEFAULT_METRICS=false

if [ -z "$DATA_SOURCE_NAME" ]; then
  echo "❌ DATA_SOURCE_NAME is empty. Check your Vault secret."
  exit 1
fi

echo "🐞 Debug info:"
echo "  - EXPORTER_USER=$EXPORTER_USER"
echo "  - EXPORTER_DB=$POSTGRES_DB"
echo "  - DATA_SOURCE_NAME=$DATA_SOURCE_NAME"

echo "🚀 Starting postgres_exporter..."
exec env DATA_SOURCE_NAME="$DATA_SOURCE_NAME" /bin/postgres_exporter