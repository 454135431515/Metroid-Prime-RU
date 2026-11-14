// Сборка мода в браузере (ADR 0006): Python (Pyodide) + код перевода, образ читается с устройства
// кусками (WORKERFS), никуда не отправляется.
importScripts("pyodide/pyodide.js");

const say = (kind, text) => postMessage({ kind, text });
let ready = null;

async function init() {
  say("log", "Загрузка Python…");
  const py = await loadPyodide({ indexURL: "pyodide/" });
  py.setStdout({ batched: (s) => say("log", s) });
  py.setStderr({ batched: (s) => say("log", s) });
  await py.loadPackage(["numpy", "pillow"], { messageCallback: () => {} });
  const files = await (await fetch("files.json")).json();
  for (const f of files) {
    const data = new Uint8Array(await (await fetch("app/" + f)).arrayBuffer());
    const path = "/app/" + f;
    py.FS.mkdirTree(path.slice(0, path.lastIndexOf("/")));
    py.FS.writeFile(path, data);
  }
  return py;
}

onmessage = async (e) => {
  try {
    ready = ready || init();
    const py = await ready;
    const file = e.data.file;
    try { py.FS.unmount("/disc"); } catch (_) {}
    py.FS.mkdirTree("/disc");
    py.FS.mount(py.FS.filesystems.WORKERFS, { files: [file] }, "/disc");
    py.globals.set("iso_path", "/disc/" + file.name);
    await py.runPythonAsync(`
import sys
sys.path.insert(0, "/app/tools")
import web_build
web_build.run(iso_path, "/out.zip", "/app")
`);
    const zip = py.FS.readFile("/out.zip");
    py.FS.unlink("/out.zip");
    postMessage({ kind: "done", zip }, [zip.buffer]);
  } catch (err) {
    // importer.fail печатает причину и выходит (SystemExit): причина уже в журнале
    const msg = String(err && err.message || err);
    say("error", /SystemExit/.test(msg) ? "" : msg.split("\n").slice(-3).join("\n"));
  }
};
