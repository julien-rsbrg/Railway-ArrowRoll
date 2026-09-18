import os
from flask import Flask, send_from_directory

app = Flask(__name__)

BUILD_DIR = os.path.join(os.path.dirname(__file__), "webgl_build")


def _add_unity_headers(resp, filename):
    name = filename
    if name.endswith(".br"):
        resp.headers["Content-Encoding"] = "br"
        name = name[:-3]
    elif name.endswith(".gz"):
        resp.headers["Content-Encoding"] = "gzip"
        name = name[:-3]

    if name.endswith(".wasm"):
        resp.headers["Content-Type"] = "application/wasm"
    elif name.endswith(".js"):
        resp.headers["Content-Type"] = "application/javascript"
    elif name.endswith(".data"):
        resp.headers["Content-Type"] = "application/octet-stream"
    return resp


@app.route("/")
def index():
    return send_from_directory(BUILD_DIR, "index.html")


@app.route("/<path:filename>")
def build_files(filename):
    resp = send_from_directory(BUILD_DIR, filename)
    return _add_unity_headers(resp, filename)


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))