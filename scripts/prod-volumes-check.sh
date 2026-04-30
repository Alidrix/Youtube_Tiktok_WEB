#!/usr/bin/env bash
set -euo pipefail

echo "ℹ️  Docker Compose services status"
docker compose --env-file .env.production -f docker-compose.prod.yml ps

echo
echo "ℹ️  Docker volumes"
docker volume ls

echo
echo "ℹ️  Project-related volumes (best effort)"
docker volume ls | grep -E "trend|scope|postgres|redis|clickhouse|nats" || true

echo
echo "ℹ️  Docker disk usage"
docker system df

echo
echo "ℹ️  Host filesystem usage"
df -h
