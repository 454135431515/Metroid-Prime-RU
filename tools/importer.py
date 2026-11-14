"""Сборщик перевода как импортёр порта (docs/MODS.md порта, «Custom importers»): программа в
`importers` рядом с `mods`; F1 > Mods > Run запускает её, порт передаёт папку модов в `MP_MODS_DIR`.

    importer [путь к ISO]

Диск ищется так: аргумент, затем `disc_path` из `port_settings.ini` (порт запоминает выбранный
образ), затем единственный `.iso` в папке пользователя или рядом с ней. Нужен Metroid Prime USA 1.00
(GM8E01, ревизия 0). Мод собирается в `<MP_MODS_DIR>/russian`; если там же лежит импорт
`remastered-models`, добавляется HD-шрифт. Код выхода 0 — мод на месте, иначе текст ошибки.
"""

import glob
import os
import shutil
import sys
import tempfile

HERE = getattr(sys, "_MEIPASS", None) or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "tools"))
import build_mod  # noqa: E402
import extract  # noqa: E402


# Порт читает вывод через pipe; на Windows Python писал бы в нём в кодировке системы (cp1252 —
# UnicodeEncodeError на русском тексте).
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):  # в браузере (Pyodide) вывод уже UTF-8
        _s.reconfigure(encoding="utf-8", errors="replace")


def fail(msg):
    print(f"Ошибка: {msg}", flush=True)
    sys.exit(1)


def ini_disc(pref):
    path = os.path.join(pref, "port_settings.ini")
    if os.path.isfile(path):
        for line in open(path, encoding="utf-8", errors="replace"):
            if line.startswith("disc_path="):
                return line.split("=", 1)[1].strip() or None
    return None


def find_disc(arg, pref):
    if arg:
        return arg
    disc = ini_disc(pref)
    if disc and os.path.isfile(disc):
        return disc
    isos = sorted({os.path.abspath(p) for d in (pref, os.path.dirname(pref))
                   for p in glob.glob(os.path.join(d, "*.iso"))})
    if len(isos) == 1:
        return isos[0]
    if isos:
        fail("рядом несколько .iso, укажите нужный в поле аргумента: " + ", ".join(isos))
    fail("не найден образ диска: выберите его в порте или укажите путь к .iso в поле аргумента")


def check_disc(path):
    if not os.path.isfile(path):
        fail(f"нет файла {path}")
    head = open(path, "rb").read(8)
    if head[:6] != b"GM8E01" or head[7] != 0:
        fail(f"{os.path.basename(path)}: нужен Metroid Prime USA 1.00 (GM8E01, ревизия 0), "
             f"а это {head[:6].decode('ascii', 'replace')} ревизия {head[7] if len(head) > 7 else '?'}")


def build_mods(disc, mods, root=HERE):
    """Мод из проверенного образа в `<mods>/russian` и `<mods>/hud-russian`; общий для импортёра
    и веб-сборки (web/, ADR 0006)."""
    work = tempfile.mkdtemp(prefix="mp-russian-")
    try:
        print("Извлечение ресурсов...", flush=True)
        extract.main(disc, work)
        print("Сборка перевода...", flush=True)
        os.chdir(root)  # build_mod берёт text/panes.json и text/port.json относительно корня
        stale = build_mod.build(os.path.join(work, "res"), os.path.join(root, "text", "ru.json"),
                                os.path.join(mods, "russian"))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    if stale:
        fail(f"{stale} строк не совпали с диском: образ не USA 1.00 или повреждён")


def main(argv):
    mods = os.environ.get("MP_MODS_DIR") or fail("MP_MODS_DIR не задан: запускайте из порта (F1 > Mods > Run)")
    mods = os.path.abspath(mods)
    pref = os.path.dirname(mods)
    disc = find_disc(argv[1] if len(argv) > 1 and argv[1].strip() else None, pref)
    check_disc(disc)
    print(f"Диск: {disc}", flush=True)
    build_mods(disc, mods)
    print("Готово: перевод в mods/russian. Перезапустите игру.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
