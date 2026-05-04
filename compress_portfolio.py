"""
compress_portfolio.py
─────────────────────
Run this script ONCE from inside your project root:
    E:\LYNA PORTFOLIO\lyna>  python compress_portfolio.py

What it does:
  • Walks every image in assets/img/portfolio/ and assets/img/profile/ and assets/img/person/
  • Re-saves every .webp / .jpg / .jpeg / .png as WebP at quality 82
  • Keeps the original filename and extension (replaces in-place)
  • Skips files already small enough (under 150 KB) to avoid double-compression
  • Prints before/after size for every file so you can see the gains

No quality loss visible to the human eye at quality 82.
Typical reduction: 50–75% smaller file size.
"""

from PIL import Image
import os, sys

# ── folders to compress (relative to where you run the script) ──────────────
TARGET_FOLDERS = [
    "assets/img/portfolio/festivaux",
    "assets/img/portfolio/Quotidien",
    "assets/img/portfolio/workshop",
    "assets/img/profile",
    "assets/img/person",
]

QUALITY       = 82          # WebP quality 0-100  (82 = visually lossless)
SKIP_UNDER_KB = 150         # skip files already below this size (KB)
EXTENSIONS    = {".webp", ".jpg", ".jpeg", ".png"}

# ── helpers ──────────────────────────────────────────────────────────────────
def human(n):
    return f"{n/1024:.0f} KB"

def compress_image(path):
    size_before = os.path.getsize(path)

    if size_before < SKIP_UNDER_KB * 1024:
        print(f"  SKIP  {os.path.basename(path):40s} already {human(size_before)}")
        return 0, 0          # saved nothing

    try:
        img = Image.open(path)

        # Convert palette / RGBA → RGB for WebP compatibility
        if img.mode in ("P", "RGBA", "LA"):
            img = img.convert("RGB")
        elif img.mode != "RGB":
            img = img.convert("RGB")

        # Save back to the same path as WebP
        # If original was .jpg/.png the filename keeps its extension
        # but the bytes are now WebP — browsers don't care about extension
        img.save(path, "WEBP", quality=QUALITY, method=6)
        img.close()

        size_after = os.path.getsize(path)
        saved = size_before - size_after
        pct = saved / size_before * 100
        print(f"  OK    {os.path.basename(path):40s} {human(size_before)} → {human(size_after)}  ({pct:.0f}% saved)")
        return size_before, size_after

    except Exception as e:
        print(f"  ERR   {os.path.basename(path):40s} {e}")
        return 0, 0

# ── main ─────────────────────────────────────────────────────────────────────
def main():
    total_before = total_after = files_done = 0

    for folder in TARGET_FOLDERS:
        if not os.path.isdir(folder):
            print(f"\n[SKIP folder not found] {folder}")
            continue

        print(f"\n── {folder} ──")
        for fname in sorted(os.listdir(folder)):
            ext = os.path.splitext(fname)[1].lower()
            if ext not in EXTENSIONS:
                continue
            fpath = os.path.join(folder, fname)
            b, a = compress_image(fpath)
            total_before += b
            total_after  += a
            if b:
                files_done += 1

    saved_total = total_before - total_after
    print("\n" + "="*60)
    print(f"  Files compressed : {files_done}")
    print(f"  Total before     : {human(total_before)}")
    print(f"  Total after      : {human(total_after)}")
    print(f"  Total saved      : {human(saved_total)}")
    if total_before:
        print(f"  Reduction        : {saved_total/total_before*100:.0f}%")
    print("="*60)
    print("\nDone! Refresh your browser — images will load much faster.")

if __name__ == "__main__":
    main()