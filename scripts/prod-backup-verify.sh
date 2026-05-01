#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-backups/postgres}"
MAX_BACKUP_AGE_HOURS="${MAX_BACKUP_AGE_HOURS:-24}"

fail() {
  echo "❌ $1"
  exit 1
}
info() {
  echo "ℹ️  $1"
}
success() {
  echo "✅ $1"
}

[ -d "$BACKUP_DIR" ] || fail "Backup directory not found: $BACKUP_DIR"

info "Latest PostgreSQL backups"
ls -lh "$BACKUP_DIR"/postgres-*.sql.gz 2>/dev/null || fail "No PostgreSQL backups found"

info "Checking gzip integrity"
for file in "$BACKUP_DIR"/postgres-*.sql.gz; do
  gzip -t "$file"
done

info "Checking SHA256 files"
for checksum in "$BACKUP_DIR"/postgres-*.sql.gz.sha256; do
  [ -f "$checksum" ] || continue
  sha256sum -c "$checksum"
done

info "Checking recent backup freshness"
if ! find "$BACKUP_DIR" -type f -name "postgres-*.sql.gz" -mmin "-$((MAX_BACKUP_AGE_HOURS * 60))" | grep -q .; then
  fail "No PostgreSQL backup newer than ${MAX_BACKUP_AGE_HOURS}h"
fi

du -sh "$BACKUP_DIR"
success "Backup verification completed"
