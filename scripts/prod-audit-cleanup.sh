#!/usr/bin/env bash
set -euo pipefail

AUDIT_RETENTION_DAYS="${AUDIT_RETENTION_DAYS:-90}"
DRY_RUN="${DRY_RUN:-1}"

fail() {
  echo "❌ $1"
  exit 1
}
info() {
  echo "ℹ️  $1"
}

[ -f .env.production ] || fail ".env.production not found"
[ -f docker-compose.prod.yml ] || fail "docker-compose.prod.yml not found"

set -a
# shellcheck disable=SC1091
source .env.production
set +a

COUNT_SQL="SELECT COUNT(*) FROM admin_audit_logs WHERE created_at < NOW() - ('${AUDIT_RETENTION_DAYS} days')::interval;"
DELETE_SQL="DELETE FROM admin_audit_logs WHERE created_at < NOW() - ('${AUDIT_RETENTION_DAYS} days')::interval;"

info "Counting admin audit logs older than ${AUDIT_RETENTION_DAYS} days"
count=$(docker compose --env-file .env.production -f docker-compose.prod.yml exec -T postgres psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -tAc "$COUNT_SQL")
info "Rows matching retention policy: ${count}"

if [ "$DRY_RUN" = "0" ]; then
  info "DRY_RUN=0: deleting old admin audit logs"
  docker compose --env-file .env.production -f docker-compose.prod.yml exec -T postgres psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -c "$DELETE_SQL" >/dev/null
  echo "✅ Cleanup completed"
else
  info "DRY_RUN=1: no rows deleted"
fi
