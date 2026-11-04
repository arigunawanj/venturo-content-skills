#!/usr/bin/env bash
# Pasang skill konten Venturo ke folder skills agent.
# Pakai: ./install.sh [claude|codex|agents|all] [--dir <folder skills custom>]
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SKILLS=(venturo-brand venturo-motion-grafik venturo-vlog venturo-ngobrol venturo-animasi-2d)
TARGET="${1:-claude}"; CUSTOM=""
if [[ "${2:-}" == "--dir" ]]; then CUSTOM="${3:?folder setelah --dir belum diisi}"; fi

install_to() {
  local dest="$1"; mkdir -p "$dest"
  for s in "${SKILLS[@]}"; do
    rm -rf "$dest/$s"; cp -R "$HERE/skills/$s" "$dest/$s"
    echo "  + $dest/$s"
  done
  chmod +x "$dest/venturo-brand/scripts/venturo.py"
}

if [[ -n "$CUSTOM" ]]; then install_to "$CUSTOM"; exit 0; fi
case "$TARGET" in
  claude) install_to "$HOME/.claude/skills" ;;
  codex)  install_to "$HOME/.codex/skills" ;;
  agents) install_to "$HOME/.agents/skills" ;;
  all)    install_to "$HOME/.claude/skills"; install_to "$HOME/.codex/skills"; install_to "$HOME/.agents/skills" ;;
  *) echo "Target tidak dikenal: $TARGET (pakai claude|codex|agents|all atau --dir <path>)"; exit 1 ;;
esac
echo "Selesai. Restart agent supaya skill baru terbaca."
