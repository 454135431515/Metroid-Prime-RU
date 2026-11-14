// Проверка веб-сборки без браузера (ADR 0006): тот же сайт, тот же Pyodide, образ через NODEFS.
//   node web/check.mjs <сайт из assemble.sh> <образ.iso> <out.zip>
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, basename, resolve } from "node:path";
import { createRequire } from "node:module";
const [site, iso, out] = process.argv.slice(2).map((p) => resolve(p));
const { loadPyodide } = createRequire(import.meta.url)(resolve(site, "pyodide/pyodide.js"));
const py = await loadPyodide({ indexURL: resolve(site, "pyodide") + "/" });
py.setStdout({ batched: (s) => console.log(s) });
await py.loadPackage(["numpy", "pillow"], { messageCallback: () => {} });
for (const f of JSON.parse(readFileSync(resolve(site, "files.json")))) {
  const p = "/app/" + f;
  py.FS.mkdirTree(p.slice(0, p.lastIndexOf("/")));
  py.FS.writeFile(p, readFileSync(resolve(site, "app", f)));
}
py.FS.mkdirTree("/disc");
py.FS.mount(py.FS.filesystems.NODEFS, { root: dirname(iso) }, "/disc");
py.globals.set("iso_path", "/disc/" + basename(iso));
await py.runPythonAsync(`
import sys
sys.path.insert(0, "/app/tools")
import web_build
web_build.run(iso_path, "/out.zip", "/app")
`);
writeFileSync(out, py.FS.readFile("/out.zip"));
console.log("check: zip ->", out);
