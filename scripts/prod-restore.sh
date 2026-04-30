#!/usr/bin/env bash
set -euo pipefail

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

require_file() {
  local file="$1"
  [ -f "$file" ] || fail "Missing required file: $file"
}

load_env() {
  require_file ".env.production"
  set -a
  # shellcheck disable=SC1091
  source .env.production
  set +a
}

main() {
  local backup_file="${1:-}"
  [ -n "$backup_file" ] || fail "Usage: ./scripts/prod-restore.sh <backup-file.sql|backup-file.sql.gz>"
  require_file "docker-compose.prod.yml"
  require_file "$backup_file"
  load_env

  case "$backup_file" in
    *.sql|*.sql.gz) ;;
    *) fail "Unsupported backup format: $backup_file (expected .sql or .sql.gz)" ;;
  esac

  if [ -f "${backup_file}.sha256" ]; then
    info "Verifying checksum..."
    sha256sum -c "${backup_file}.sha256"
  else
    info "No checksum file found for ${backup_file}; skipping verification"
  fi

  if [ "${YES:-0}" != "1" ]; then
    read -r -p "This will restore database from ${backup_file}. Continue? [y/N] " confirm
    if [ "$confirm" != "y" ]; then
      info "Restore cancelled"
      exit 0
    fi
  fi

  if [ "${SKIP_PRE_RESTORE_BACKUP:-0}" != "1" ]; then
    info "Creating safety backup before restore..."
    ./scripts/prod-backup.sh
  fi

  info "Restoring database from ${backup_file}..."
  if [[ "$backup_file" == *.sql.gz ]]; then
    gzip -dc "$backup_file" | docker compose --env-file .env.production -f docker-compose.prod.yml exec -T postgres \
      psql -U "${POSTGRES_USER:-viral}" "${POSTGRES_DB:-viral_radar}"
  else
    docker compose --env-file .env.production -f docker-compose.prod.yml exec -T postgres \
      psql -U "${POSTGRES_USER:-viral}" "${POSTGRES_DB:-viral_radar}" < "$backup_file"
  fi

  success "Restore completed from $backup_file"
}

main "$@"
