#!/usr/bin/with-contenv bashio
set -euo pipefail

export BRIDGE_ACCESS_TOKEN="$(bashio::config 'access_token')"
export SUPERVISOR_TOKEN="${SUPERVISOR_TOKEN:?Supervisor token was not injected}"
export ALLOW_CORE_RESTART="$(bashio::config 'allow_core_restart')"
export ALLOW_APP_MANAGEMENT="$(bashio::config 'allow_app_management')"
export ALLOW_BACKUP_RESTORE="$(bashio::config 'allow_backup_restore')"
export ALLOW_LOG_READ="$(bashio::config 'allow_log_read')"
export ALLOW_HACS_MANAGEMENT="$(bashio::config 'allow_hacs_management')"

if bashio::var.is_empty "${BRIDGE_ACCESS_TOKEN}"; then
  bashio::log.error "Configure a bridge access token before starting."
  exit 1
fi

exec python3 /bridge.py
