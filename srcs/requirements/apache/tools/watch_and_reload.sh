#!/bin/sh

echo "👁️ Watch SSL certificats Apache..."

inotifywait -mq -e close_write \
  /etc/apache2/ssl/apache.crt \
  /etc/apache2/ssl/apache.key |
while read path action file; do
  echo "🔁 Certificat modify: $file – reload Apache"

  PIDS=$(ps -eo pid,comm,user | grep httpd | grep apache | awk '{print $1}')
  if [ -n "$PIDS" ]; then
    for PID in $PIDS; do
      echo "🔁 Reload Apache PID: $PID"
      kill -1 "$PID"
    done
    echo "✅ Apache reloaded"
  else
    echo "❌ Apache process not found"
  fi
done
