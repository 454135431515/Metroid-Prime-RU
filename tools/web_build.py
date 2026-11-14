"""Сборка мода в браузере (Pyodide, ADR 0006): образ игрока -> zip с `russian` и `hud-russian`.

Вызывает web/worker.js; код сборки тот же, что у импортёра (importer.build_mods).
    python -I tools/web_build.py <образ.iso> <out.zip>   # то же самое без браузера
"""

import os
import shutil
import sys
import tempfile
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import build_mod  # noqa: E402
import importer  # noqa: E402


def run(iso, out_zip, root=ROOT):
    importer.check_disc(iso)
    mods = tempfile.mkdtemp(prefix="mp-russian-mods-")
    try:
        importer.build_mods(iso, mods, root)
        pack(mods, out_zip)
    finally:
        shutil.rmtree(mods, ignore_errors=True)
    print("Готово: распакуйте архив в папку mods порта.", flush=True)


def pack(mods, out_zip):
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for top in ("russian", build_mod.FRAMES_MOD):
            for d, _, names in sorted(os.walk(os.path.join(mods, top))):
                for n in sorted(names):
                    p = os.path.join(d, n)
                    z.write(p, os.path.relpath(p, mods))


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
