#!/bin/sh

echo "Applying database migrations..."
python3 manage.py migrate
echo "✓ All database migrations are applied"

# Start Django server
echo "Starting Django server..."
python3 manage.py runserver 0.0.0.0:8000
