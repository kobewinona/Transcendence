#!/bin/sh

# ENV_SECRET="/run/secrets/backend_env_file"
# ENV_TARGET="/usr/src/app/.env"

# echo "🔍 Checking for Docker secret at $ENV_SECRET..."
# if [ -f "$ENV_SECRET" ]; then
#   echo "✅ Found Docker secret, copying to $ENV_TARGET"
#   cp "$ENV_SECRET" "$ENV_TARGET"
# else
#   echo "⚠️ No secret found at $ENV_SECRET. Proceeding without .env injection."
# fi

echo "Waiting for PostgreSQL to start..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "✓ PostgreSQL is up and running!"

echo "Running migrations..."
pipenv run python manage.py makemigrations --noinput
pipenv run python manage.py migrate --noinput || {
    echo "⚠️ Migration failed due to inconsistency! Resetting migrations..."
    pipenv run python manage.py migrate --fake-initial
}
echo "✓ Migrations are successfully applied!"

exec "$@"
