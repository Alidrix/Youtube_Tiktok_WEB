#!/usr/bin/env bash
set -euo pipefail
BACKUP_DIR="${BACKUP_DIR:-backups/postgres}"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "ℹ️  Creating PostgreSQL backup..."
docker compose --env-file .env.production -f docker-compose.prod.yml exec -T postgres \
  pg_dump -U "${POSTGRES_USER:-viral}" "${POSTGRES_DB:-viral_radar}" \
  > "${BACKUP_DIR}/postgres-${TIMESTAMP}.sql"
echo "✅ Backup written to ${BACKUP_DIR}/postgres-${TIMESTAMP}.sql"
