#!/usr/bin/env python3
"""Gallery folder -> web assets (webp stills, mp4 loops) + assets/gallery/manifest.js.

Usage: tools/build_gallery.py [SRC_DIR]   (needs magick + ffmpeg on PATH)
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "Valor Cat - Series/www/spectra-render/Gallery"
OUT = SITE / "assets/gallery"
STILL = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}
VIDEO = {".mov", ".mp4", ".mkv", ".webm"}


def run(*cmd: str) -> str:
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def title_of(stem: str) -> str:
    return re.sub(r"[_\-]+", " ", re.sub(r"^(INT|EXT|CHR)_", "", stem)).strip()


def dims(path: Path) -> tuple[int, int]:
    w, h = run("magick", "identify", "-format", "%w %h", f"{path}[0]").split()
    return int(w), int(h)


def build_still(src: Path, key: str, crop: int) -> dict:
    full, thumb = OUT / f"{key}.webp", OUT / f"{key}-thumb.webp"
    pre = ["magick", str(src), "-colorspace", "sRGB"]
    if crop:
        pre += ["-gravity", "North", "-chop", f"0x{crop}"]
    if not full.exists() or full.stat().st_mtime < src.stat().st_mtime:
        run(*pre, "-resize", "2400x2400>", "-quality", "86", str(full))
        run(*pre, "-resize", "960x960>", "-quality", "80", str(thumb))
    w, h = dims(full)
    return {"type": "image", "src": f"assets/gallery/{full.name}", "thumb": f"assets/gallery/{thumb.name}", "w": w, "h": h}


def build_video(src: Path, key: str, crop: int) -> dict:
    mp4, poster = OUT / f"{key}.mp4", OUT / f"{key}-poster.webp"
    vf = (f"crop=iw:ih-{crop}:0:{crop}," if crop else "") + "scale='min(1280,iw)':-2,format=yuv420p"
    if not mp4.exists() or mp4.stat().st_mtime < src.stat().st_mtime:
        run("ffmpeg", "-v", "error", "-y", "-i", str(src), "-an", "-vf", vf, "-c:v", "libx264",
            "-preset", "slow", "-crf", "24", "-movflags", "+faststart", str(mp4))
        run("ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", str(mp4), "-frames:v", "1", "-q:v", "80", str(poster))
    w, h = dims(poster)
    return {"type": "video", "src": f"assets/gallery/{mp4.name}", "thumb": f"assets/gallery/{poster.name}", "w": w, "h": h}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cfg = json.loads((SITE / "gallery.json").read_text())["items"]
    listed = {c["src"] for c in cfg}
    extras = [{"src": p.name} for p in sorted(SRC.iterdir())
              if p.suffix.lower() in STILL | VIDEO and p.name not in listed]
    manifest = []
    for item in cfg + extras:
        src = SRC / item["src"]
        if not src.exists():
            print(f"skip (missing): {src}", file=sys.stderr)
            continue
        key, crop = slug(src.stem), int(item.get("crop_top", 0))
        built = (build_video if src.suffix.lower() in VIDEO else build_still)(src, key, crop)
        manifest.append(built | {"title": item.get("title") or title_of(src.stem),
                                 "caption": item.get("caption", ""), "tag": item.get("tag", "")})
        print(f"ok  {src.name} -> {built['src']}")
    (OUT / "manifest.js").write_text("window.GALLERY = " + json.dumps(manifest, indent=1) + ";\n")


if __name__ == "__main__":
    main()
