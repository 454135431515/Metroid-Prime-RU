#!/bin/sh
# Импортёр перевода одним исполняемым файлом (без Python у игрока): dist/russian[.exe].
# Нужны PyInstaller, Pillow, numpy в текущем Python. Собирает под ту ОС, где запущен.
set -e
# Пути относительные: spec пишется в корень (russian.spec), а абсолютный $PWD Git Bash на Windows
# передаёт Python в виде /d/a/..., который PyInstaller не находит.
cd "$(dirname "$0")/.."
sep=":"; case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) sep=";";; esac
python -m PyInstaller --onefile --name russian --distpath dist --workpath build/freeze \
  --paths tools --add-data "text/ru.json${sep}text" --add-data "text/panes.json${sep}text" --add-data "text/port.json${sep}text" --add-data "tools/glyphs${sep}glyphs" --add-data "tools/pixel${sep}pixel" \
  --log-level WARN tools/importer.py
