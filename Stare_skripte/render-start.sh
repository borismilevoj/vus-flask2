#!/usr/bin/env bash
set -euo pipefail
mkdir -p /var/data

if [[ -n "${VUS_DB_URL:-}" ]]; then
  echo "[start] prenos VUS.db …"
  tmp="$(mktemp /var/data/VUS.tmp.XXXXXX)"
  curl -fL --retry 3 -o "$tmp" "$VUS_DB_URL"

  # integriteta SQLite
  python - "$tmp" <<'PY'
import sqlite3, sys
p=sys.argv[1]
con = sqlite3.connect(p)
ok  = con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
con.close()
raise SystemExit(0 if ok else 1)
PY

  ts="$(date +%Y%m%d-%H%M%S)"
  [[ -f /var/data/VUS.db ]] && cp -v /var/data/VUS.db "/var/data/VUS_${ts}.db.bak" || true
  mv -v "$tmp" /var/data/VUS.db
  echo "[start] VUS.db posodobljen."
else
  echo "[start] VUS_DB_URL ni nastavljen – preskakujem prenos."
fi

exec gunicorn -b 0.0.0.0:${PORT:-10000} app:app
