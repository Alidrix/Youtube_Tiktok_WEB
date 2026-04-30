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

cleanup_old_backups() {
  local dir="$1"
  local retention_days="${BACKUP_RETENTION_DAYS:-14}"

  find "$dir" -type f -name "postgres-*.sql.gz" -mtime +"$retention_days" -print -delete || true
  find "$dir" -type f -name "postgres-*.sql.gz.sha256" -mtime +"$retention_days" -print -delete || true
}

main() {
  require_file "docker-compose.prod.yml"
  load_env

  local backup_dir="${BACKUP_DIR:-backups/postgres}"
  local timestamp
  timestamp="$(date +%Y%m%d-%H%M%S)"
  local output="${backup_dir}/postgres-${timestamp}.sql.gz"

  mkdir -p "$backup_dir"

  info "Creating compressed PostgreSQL backup..."

  docker compose --env-file .env.production -f docker-compose.prod.yml exec -T postgres \
    pg_dump -U "${POSTGRES_USER:-viral}" "${POSTGRES_DB:-viral_radar}" \
    | gzip -9 > "$output"

  sha256sum "$output" > "${output}.sha256"

  success "Backup written to $output"
  du -h "$output"

  cleanup_old_backups "$backup_dir"
}

main "$@"
