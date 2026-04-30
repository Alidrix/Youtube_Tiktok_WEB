#!/usr/bin/env bash
set -euo pipefail
BACKUP_FILE="${1:-}"
if [ -z "$BACKUP_FILE" ]; then echo "Usage: ./scripts/prod-restore.sh <backup-file.sql>"; exit 1; fi
if [ ! -f "$BACKUP_FILE" ]; then echo "Backup file not found: $BACKUP_FILE"; exit 1; fi
if [ "${YES:-0}" != "1" ]; then
  read -r -p "This will restore database from ${BACKUP_FILE}. Continue? [y/N] " confirm
  if [ "$confirm" != "y" ]; then echo "Restore cancelled"; exit 0; fi
fi
docker compose --env-file .env.production -f docker-compose.prod.yml exec -T postgres \
  psql -U "${POSTGRES_USER:-viral}" "${POSTGRES_DB:-viral_radar}" < "$BACKUP_FILE"
echo "✅ Restore completed from $BACKUP_FILE"
