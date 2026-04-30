#!/usr/bin/env bash
set -euo pipefail
set -a; [ -f .env.production ] && . ./.env.production; set +a
BACKUP_DIR="${BACKUP_DIR:-backups/exports}"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
EXPORTS_DIR="${LOCAL_EXPORTS_DIR:-exports}"
mkdir -p "$BACKUP_DIR"
tar -czf "${BACKUP_DIR}/exports-${TIMESTAMP}.tar.gz" "$EXPORTS_DIR"
echo "✅ Exports backup written to ${BACKUP_DIR}/exports-${TIMESTAMP}.tar.gz"
