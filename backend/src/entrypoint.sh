#!/bin/sh
set -e

echo "📦 Running makemigrations..."
uv run manage.py makemigrations

echo "📦 Running migrations..."
uv run manage.py migrate --noinput

echo "🎨 Collecting static files..."
uv run manage.py collectstatic --noinput

echo "🔍 Rebuilding Elasticsearch indexes..."
yes y | uv run manage.py search_index --rebuild

echo "🚀 Starting Daphne..."
exec uv run daphne -b 0.0.0.0 -p 8000 config.asgi:application
