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

  find "$dir" -type f -name "exports-*.tar.gz" -mtime +"$retention_days" -print -delete || true
  find "$dir" -type f -name "exports-*.tar.gz.sha256" -mtime +"$retention_days" -print -delete || true
}

main() {
  load_env

  local backup_dir="${BACKUP_DIR:-backups/exports}"
  local timestamp
  timestamp="$(date +%Y%m%d-%H%M%S)"
  local exports_dir="${LOCAL_EXPORTS_DIR:-exports}"
  local output="${backup_dir}/exports-${timestamp}.tar.gz"

  if [ ! -d "$exports_dir" ]; then
    echo "⚠️  Exports directory does not exist, creating it: $exports_dir"
    mkdir -p "$exports_dir"
  fi

  mkdir -p "$backup_dir"
  tar -czf "$output" "$exports_dir"
  sha256sum "$output" > "${output}.sha256"

  success "Exports backup written to $output"

  cleanup_old_backups "$backup_dir"
}

main "$@"
