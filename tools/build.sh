#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
CC65_ROOT="${CC65_ROOT:-/workspace/tools/cc65}"
mkdir -p dist build
python3 tools/art.py
"$CC65_ROOT/bin/cl65" -t apple2enh -C "$CC65_ROOT/cfg/apple2enh-hgr.cfg" -O \
  -m dist/proch.map -Ln dist/proch.lbl -o dist/PROCH src/game.c src/mouse.s
python3 tools/disk.py
python3 tests/test_disk.py
