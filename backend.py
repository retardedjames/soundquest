#!/usr/bin/env python3
"""Soundquest removed-song persistence service.

Keeps a JSON-line file of song filenames the user has swiped away.
Tiny FastAPI app behind nginx; no DB, no auth — this is a personal app.
"""
import json
import os
import threading
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel, Field

DATA_DIR = Path(os.environ.get("SQ_DATA_DIR", "/var/lib/soundquest"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
REMOVED_FILE = DATA_DIR / "removed.json"

_lock = threading.Lock()


def _load():
    if not REMOVED_FILE.exists():
        return []
    try:
        return json.loads(REMOVED_FILE.read_text())
    except Exception:
        return []


def _save(items):
    tmp = REMOVED_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(items, ensure_ascii=False))
    tmp.replace(REMOVED_FILE)


app = FastAPI(title="Soundquest", version="1.0")


class RemoveReq(BaseModel):
    filename: str = Field(min_length=1, max_length=512)


@app.get("/api/removed")
def removed():
    with _lock:
        return {"removed": _load()}


@app.post("/api/remove")
def remove(req: RemoveReq):
    with _lock:
        items = _load()
        if req.filename not in items:
            items.append(req.filename)
            _save(items)
        return {"ok": True, "count": len(items)}


@app.get("/api/health")
def health():
    return {"ok": True}
