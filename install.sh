#!/usr/bin/env bash
# Pasang skill konten Venturo ke folder skills agent.
#
# Satu baris (tanpa clone manual):
#   curl -fsSL https://raw.githubusercontent.com/arigunawanj/venturo-content-skills/main/install.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/arigunawanj/venturo-content-skills/main/install.sh | bash -s -- all --deps
#
# Dari folder repo:
#   ./install.sh [claude|codex|agents|all] [--deps] [--dir <folder skills custom>]
#   --deps  ikut memasang kebutuhan: numpy scipy pillow playwright faster-whisper + Chromium
set -euo pipefail
REPO="${VENTURO_REPO:-https://github.com/arigunawanj/venturo-content-skills.git}"
SKILLS=(venturo-brand venturo-motion-grafik venturo-vlog venturo-ngobrol venturo-animasi-2d)

TARGET="claude"; CUSTOM=""; DEPS=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    claude|codex|agents|all) TARGET="$1" ;;
    --deps) DEPS=1 ;;
    --dir) CUSTOM="${2:?folder setelah --dir belum diisi}"; shift ;;
    x) ;;  # kompatibel dengan pola lama: ./install.sh x --dir <path>
    *) echo "Opsi tidak dikenal: $1"; exit 1 ;;
  esac
  shift
done

# Sumber skill: folder repo ini, atau clone sementara bila dijalankan lewat curl | bash
SRC=""
if [[ -n "${BASH_SOURCE[0]:-}" && -f "${BASH_SOURCE[0]}" ]]; then
  HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  [[ -d "$HERE/skills/venturo-brand" ]] && SRC="$HERE"
fi
if [[ -z "$SRC" ]]; then
  command -v git >/dev/null || { echo "git belum terpasang. Instal git dulu."; exit 1; }
  TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
  echo "Mengambil skill dari $REPO ..."
  if ! git clone --quiet --depth 1 "$REPO" "$TMP/repo"; then
    echo "Gagal mengambil repo. Kalau repo private, pastikan akun GitHub ini sudah diundang sebagai collaborator"
    echo "dan sudah login (mis. 'gh auth login' atau git credential), lalu ulangi."
    exit 1
  fi
  SRC="$TMP/repo"
fi

install_to() {
  local dest="$1"; mkdir -p "$dest"
  for s in "${SKILLS[@]}"; do
    rm -rf "${dest:?}/$s"; cp -R "$SRC/skills/$s" "$dest/$s"
    echo "  + $dest/$s"
  done
  chmod +x "$dest/venturo-brand/scripts/venturo.py"
}

if [[ -n "$CUSTOM" ]]; then install_to "$CUSTOM"
else
  case "$TARGET" in
    claude) install_to "$HOME/.claude/skills" ;;
    codex)  install_to "$HOME/.codex/skills" ;;
    agents) install_to "$HOME/.agents/skills" ;;
    all)    install_to "$HOME/.claude/skills"; install_to "$HOME/.codex/skills"; install_to "$HOME/.agents/skills" ;;
  esac
fi

if [[ "$DEPS" == 1 ]]; then
  echo "Memasang kebutuhan Python + Chromium ..."
  command -v ffmpeg >/dev/null || echo "  ! ffmpeg belum ada: macOS 'brew install ffmpeg', Ubuntu 'sudo apt install ffmpeg'"
  PIP="python3 -m pip install --user"
  $PIP numpy scipy pillow playwright faster-whisper 2>/dev/null || python3 -m pip install --break-system-packages numpy scipy pillow playwright faster-whisper
  python3 -m playwright install chromium
fi
echo "Selesai. Restart agent supaya skill Venturo terbaca."
