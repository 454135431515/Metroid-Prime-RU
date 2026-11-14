#!/bin/sh
# Сайт веб-сборки (ADR 0006): страница, Python для браузера (Pyodide) и код сборки.
#   sh web/assemble.sh <папка npm-пакета pyodide> <папка с колёсами numpy и pillow> <выходная папка>
# Только код и перевод из репозитория; данных Nintendo нет (text/en.json не копируется).
set -e
cd "$(dirname "$0")/.."
pyo=$1; wheels=$2; out=$3
rm -rf "$out"; mkdir -p "$out/pyodide" "$out/app/tools" "$out/app/text"
cp web/index.html web/worker.js "$out/"
for f in pyodide.js pyodide.asm.js pyodide.asm.wasm python_stdlib.zip pyodide-lock.json; do cp "$pyo/$f" "$out/pyodide/"; done
cp "$wheels"/numpy-*.whl "$wheels"/pillow-*.whl "$out/pyodide/"
for f in tools/*.py; do case "$(basename "$f")" in test_*) ;; *) cp "$f" "$out/app/tools/";; esac; done
cp -r tools/glyphs tools/pixel "$out/app/tools/"
cp text/ru.json text/panes.json text/port.json "$out/app/text/"
(cd "$out/app" && find . -type f | sed 's#^\./##' | sort | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().split()))') > "$out/files.json"
echo "web: $out ($(du -sh "$out" | cut -f1))"
