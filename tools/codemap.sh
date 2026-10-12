#!/usr/bin/env bash
# Prints a compact map of index.html (functions + main sections, with line numbers)
# so Claude can Read only the lines it needs instead of the whole 100 KB file.
f="${1:-$(dirname "$0")/../index.html}"
echo "== sections =="; grep -nE '<style|</style>|<script|</script>|<body|class="(sheet|ov)' "$f" | cut -c1-90
echo "== functions =="; grep -noE '(async )?function [A-Za-z0-9_$]+|^\s*(const|let) [A-Za-z0-9_$]+ ?= ?(async )?\([^)]*\) ?=>' "$f" \
  | sed -E 's/(async )?function //; s/^([0-9]+):\s*(const|let) ([A-Za-z0-9_$]+).*/\1:\3/' | paste -sd' ' | fold -w 120 -s
