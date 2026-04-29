#!/usr/bin/env python3
"""Build index.html with the song list embedded."""
import json, re, pathlib

ROOT = pathlib.Path(__file__).parent
songs = json.loads((ROOT / "songs.json").read_text())
template = (ROOT / "index.template.html").read_text()
out = template.replace("__SONGS_JSON__", json.dumps(songs, ensure_ascii=False))
(ROOT / "index.html").write_text(out)
print(f"Built index.html with {len(songs)} songs ({len(out)} bytes)")
