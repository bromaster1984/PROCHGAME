#!/usr/bin/env bash
set -euo pipefail
CC65_ROOT="${CC65_ROOT:-/workspace/tools/cc65}"
CC65_REV=52727a5b407bfeac0dfac1fdd84be8cd2af4f814
if [ ! -d "$CC65_ROOT/.git" ]; then
  mkdir -p "$(dirname "$CC65_ROOT")"
  git clone https://github.com/cc65/cc65.git "$CC65_ROOT"
  git -C "$CC65_ROOT" checkout "$CC65_REV"
fi
if [ "$(git -C "$CC65_ROOT" rev-parse HEAD)" != "$CC65_REV" ]; then
  echo 'Existing cc65 checkout has a different revision; select a separate CC65_ROOT.' >&2
  exit 1
fi
make -C "$CC65_ROOT" -j4 > /tmp/proch-cc65-build.log 2>&1
python3 -c 'from PIL import Image, ImageDraw'
