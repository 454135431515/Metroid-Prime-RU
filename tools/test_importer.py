"""Импортёр находит диск по port_settings.ini и отказывается от чужого образа.

    python -I tools/test_importer.py
"""

import glob
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importer  # noqa: E402


def main():
    with tempfile.TemporaryDirectory() as d:
        iso = os.path.join(d, "game.iso")
        open(iso, "wb").write(b"GM8E01\x00\x00" + bytes(32))
        open(os.path.join(d, "port_settings.ini"), "w").write(f"aspect=4:3\ndisc_path={iso}\n")
        assert importer.ini_disc(d) == iso
        assert importer.find_disc(None, d) == iso
        importer.check_disc(iso)  # ревизия 0 — проходит
        open(iso, "r+b").write(b"GM8E01\x00\x02")
        r = subprocess.run([sys.executable, "-I", importer.__file__, iso], capture_output=True, text=True,
                           env=dict(os.environ, MP_MODS_DIR=os.path.join(d, "mods")))
        assert r.returncode == 1 and "ревизия 2" in r.stdout, r.stdout
    # всё, что сборка читает из text/, лежит в собранном импортёре (freeze.sh); en.json — данные
    # Nintendo, сборка его не читает (v1.0.0 вышел без port.json: issue #1)
    tools = os.path.dirname(os.path.abspath(__file__))
    used = {m for p in glob.glob(os.path.join(tools, "*.py")) if not os.path.basename(p).startswith("test_")
            for m in re.findall(r'"(text/[a-z_]+\.json)"', open(p, encoding="utf-8").read())} - {"text/en.json"}
    freeze = open(os.path.join(tools, "freeze.sh"), encoding="utf-8").read()
    assert used and all(f'"{u}$' in freeze for u in used), sorted(u for u in used if f'"{u}$' not in freeze)
    print("importer: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
