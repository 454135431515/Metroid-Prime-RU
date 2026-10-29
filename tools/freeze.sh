#!/bin/sh
# Импортёр перевода одним исполняемым файлом (без Python у игрока): dist/russian[.exe].
# Нужны PyInstaller, Pillow, numpy в текущем Python. Собирает под ту ОС, где запущен.
set -e
cd "$(dirname "$0")/.."
sep=":"; case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) sep=";";; esac
python -m PyInstaller --onefile --name russian --distpath dist --workpath build/freeze --specpath build \
  --paths tools --add-data "$PWD/text/ru.json${sep}text" --add-data "$PWD/text/panes.json${sep}text" \
  --log-level WARN tools/importer.py
