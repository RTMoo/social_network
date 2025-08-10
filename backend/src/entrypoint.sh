#!/bin/sh
set -e

# Ждём, пока Elasticsearch поднимется
echo "⏳ Waiting for Elasticsearch..."
until curl -s http://elasticsearch:9200 >/dev/null; do
  sleep 2
done

# Создаём индексы Elasticsearch
echo "⚡ Creating Elasticsearch indexes..."
yes y | uv run manage.py search_index --rebuild

# Запускаем сервер Django
echo "🚀 Starting Django server..."
exec uv run manage.py runserver 0.0.0.0:8000
