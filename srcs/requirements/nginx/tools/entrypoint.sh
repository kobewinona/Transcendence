#!/bin/sh
set -e

echo "🔧 Setting correct permissions for SSL certificates..."
chown -R www-data:www-data /vault/certs
chmod 644 /vault/certs/*

echo "🔧 Ensuring Nginx logs are writable..."
chown -R www-data:www-data /var/log/nginx /var/log/modsecurity
chmod -R 755 /var/log/nginx /var/log/modsecurity

echo "🚀 Starting Nginx..."
exec nginx -g "daemon off;"