#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""斌哥照片播放器 — 本機維護伺服器。

主題 = Library/ 底下的資料夾名稱。
匯入照片 → 寫入對應資料夾；首頁列出全部主題供播放。

用法：
  python3 server.py
  開啟 http://127.0.0.1:8765/
"""

from __future__ import annotations

import json
import mimetypes
import re
import shutil
import sys
import webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote, urlparse, parse_qs

ROOT = Path(__file__).resolve().parent
LIBRARY = ROOT / "Library"
WEB = ROOT
HOST = "127.0.0.1"
PORT = 8765
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".heic"}

SAFE_THEME = re.compile(r"^[\w\u4e00-\u9fff\u3400-\u4dbf\- ·・（）()＋+&]{1,60}$")


def ensure_library() -> None:
    LIBRARY.mkdir(parents=True, exist_ok=True)


def theme_path(name: str) -> Path | None:
    name = (name or "").strip()
    if not name or not SAFE_THEME.match(name):
        return None
    if name in (".", "..") or "/" in name or "\\" in name:
        return None
    return LIBRARY / name


def list_photos(folder: Path) -> list[Path]:
    if not folder.is_dir():
        return []
    out = []
    for p in folder.iterdir():
        if p.is_file() and p.suffix.lower() in IMG_EXT and not p.name.startswith("."):
            out.append(p)
    return sorted(out, key=lambda x: x.name.lower())


def themes_payload() -> list[dict]:
    ensure_library()
    items = []
    for d in sorted(LIBRARY.iterdir(), key=lambda p: p.name.lower()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        photos = list_photos(d)
        items.append({"name": d.name, "count": len(photos)})
    return items


def safe_filename(name: str) -> str:
    name = Path(name).name
    keep = []
    for c in name:
        if c.isalnum() or c in "._- ()（）+":
            keep.append(c)
        else:
            keep.append("_")
    out = "".join(keep).strip("._") or "photo.jpg"
    if not Path(out).suffix:
        out += ".jpg"
    return out[:160]


def _is_under(path: Path, root: Path) -> bool:
    """True if path resolves under root (Python 3.8+ safe)."""
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))

    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code: int, obj) -> None:
        raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self._send(code, raw, "application/json; charset=utf-8")

    def _read_json(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0:
            return {}
        raw = self.rfile.read(n)
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return {}

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        if path == "/api/themes":
            self._json(200, {"themes": themes_payload()})
            return

        if path.startswith("/api/themes/") and path.endswith("/photos"):
            name = unquote(path[len("/api/themes/") : -len("/photos")])
            folder = theme_path(name)
            if folder is None or not folder.is_dir():
                self._json(404, {"error": "主題不存在"})
                return
            photos = []
            for p in list_photos(folder):
                photos.append(
                    {
                        "name": p.name,
                        "url": "/library/%s/%s" % (name, p.name),
                        "caption": p.stem,
                    }
                )
            self._json(200, {"name": name, "count": len(photos), "photos": photos})
            return

        if path.startswith("/library/"):
            rel = path[len("/library/") :]
            parts = rel.split("/", 1)
            if len(parts) != 2:
                self.send_error(404)
                return
            theme, filename = parts[0], parts[1]
            folder = theme_path(unquote(theme))
            if folder is None:
                self.send_error(404)
                return
            fpath = folder / Path(unquote(filename)).name
            if not fpath.is_file() or not _is_under(fpath, LIBRARY):
                self.send_error(404)
                return
            ctype = mimetypes.guess_type(str(fpath))[0] or "application/octet-stream"
            data = fpath.read_bytes()
            self._send(200, data, ctype)
            return

        # static pages
        if path in ("/", "/index.html"):
            fpath = WEB / "index.html"
        elif path in ("/maintain", "/maintain.html"):
            fpath = WEB / "maintain.html"
        elif path.startswith("/") and ".." not in path:
            fpath = WEB / path.lstrip("/")
        else:
            self.send_error(404)
            return

        if not fpath.is_file():
            self.send_error(404)
            return
        ctype = mimetypes.guess_type(str(fpath))[0] or "application/octet-stream"
        if fpath.suffix.lower() in {".html", ".js", ".css", ".txt", ".md"}:
            ctype = {
                ".html": "text/html; charset=utf-8",
                ".js": "application/javascript; charset=utf-8",
                ".css": "text/css; charset=utf-8",
                ".txt": "text/plain; charset=utf-8",
                ".md": "text/markdown; charset=utf-8",
            }.get(fpath.suffix.lower(), ctype)
        self._send(200, fpath.read_bytes(), ctype)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        if path == "/api/themes":
            body = self._read_json()
            name = (body.get("name") or "").strip()
            folder = theme_path(name)
            if folder is None:
                self._json(400, {"error": "主題名稱無效（勿含路徑符號，最長 60 字）"})
                return
            if folder.exists():
                self._json(200, {"ok": True, "name": name, "created": False})
                return
            folder.mkdir(parents=True, exist_ok=False)
            self._json(201, {"ok": True, "name": name, "created": True})
            return

        if path.startswith("/api/themes/") and path.endswith("/photos"):
            name = unquote(path[len("/api/themes/") : -len("/photos")])
            folder = theme_path(name)
            if folder is None:
                self._json(400, {"error": "主題名稱無效"})
                return
            folder.mkdir(parents=True, exist_ok=True)
            ctype = self.headers.get("Content-Type", "")
            if "multipart/form-data" not in ctype:
                self._json(400, {"error": "請用 multipart 上傳"})
                return
            saved, skipped = self._save_multipart(folder, ctype)
            self._json(
                200,
                {
                    "ok": True,
                    "name": name,
                    "saved": saved,
                    "skipped": skipped,
                    "count": len(list_photos(folder)),
                },
            )
            return

        self._json(404, {"error": "not found"})

    def do_DELETE(self) -> None:
        path = unquote(urlparse(self.path).path)
        if not path.startswith("/api/themes/"):
            self._json(404, {"error": "not found"})
            return
        name = path[len("/api/themes/") :].strip("/")
        if "/photos/" in name:
            # DELETE /api/themes/{name}/photos/{filename}
            theme, _, filename = name.partition("/photos/")
            folder = theme_path(theme)
            if folder is None or not folder.is_dir():
                self._json(404, {"error": "主題不存在"})
                return
            fpath = folder / Path(unquote(filename)).name
            if fpath.is_file():
                fpath.unlink()
            self._json(200, {"ok": True, "count": len(list_photos(folder))})
            return
        folder = theme_path(name)
        if folder is None or not folder.is_dir():
            self._json(404, {"error": "主題不存在"})
            return
        shutil.rmtree(folder)
        self._json(200, {"ok": True, "deleted": name})

    def _save_multipart(self, folder: Path, content_type: str) -> tuple[int, int]:
        """Minimal multipart parser for file fields named 'files' or 'file'."""
        m = re.search(r"boundary=(.+)", content_type)
        if not m:
            return 0, 0
        boundary = m.group(1).strip().strip('"').encode("utf-8")
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n)
        parts = raw.split(b"--" + boundary)
        saved = 0
        skipped = 0
        for part in parts:
            if b"Content-Disposition" not in part:
                continue
            header, _, body = part.partition(b"\r\n\r\n")
            if not body:
                continue
            if body.endswith(b"\r\n"):
                body = body[:-2]
            if body.endswith(b"--"):
                body = body[:-2]
            if body.endswith(b"\r\n"):
                body = body[:-2]
            hm = re.search(br'filename="([^"]+)"', header)
            if not hm:
                continue
            fname = hm.group(1).decode("utf-8", errors="replace")
            fname = safe_filename(fname)
            if Path(fname).suffix.lower() not in IMG_EXT:
                skipped += 1
                continue
            dest = folder / fname
            if dest.exists():
                stem, suf = dest.stem, dest.suffix
                i = 2
                while dest.exists():
                    dest = folder / f"{stem}_{i}{suf}"
                    i += 1
            dest.write_bytes(body)
            saved += 1
        return saved, skipped


def main() -> None:
    ensure_library()
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    url = "http://%s:%d/" % (HOST, PORT)
    print("═" * 50)
    print("  斌哥照片播放器")
    print("  首頁／播放：%s" % url)
    print("  匯入維護：http://%s:%d/maintain.html" % (HOST, PORT))
    print("  Library：%s" % LIBRARY)
    print("  Ctrl+C 結束")
    print("═" * 50)
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止")
        server.server_close()


if __name__ == "__main__":
    main()
