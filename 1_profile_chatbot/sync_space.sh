#!/usr/bin/env bash
# Copy deployable sources into space/ so Gradio/HF upload a self-contained folder.
# Edit files in the parent directory, then re-run this before each deploy.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
DEST="$ROOT/space"

mkdir -p "$DEST"

rsync -a --delete \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  "$ROOT/agent/" "$DEST/agent/"

cp "$ROOT/requirements.txt" "$DEST/requirements.txt"
cp "$ROOT/summary.txt" "$DEST/summary.txt"

if [[ -f "$ROOT/linkedin.pdf" ]]; then
  cp "$ROOT/linkedin.pdf" "$DEST/linkedin.pdf"
else
  echo "warning: linkedin.pdf not found — Space will run on summary.txt only" >&2
  rm -f "$DEST/linkedin.pdf"
fi

echo "Synced into $DEST:"
ls -la "$DEST"
