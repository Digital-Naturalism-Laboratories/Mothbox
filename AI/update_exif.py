import csv
import json
import re
import subprocess
import threading
from pathlib import Path
import os
import platform

# ── CONFIG ────────────────────────────────────────────────────────────────────

CSV_PATH = r"D:/MothboxData_Hubert/data/Panama/Azuero_EcoVenaoAZ017_flatHapuku_2025-04-11/2025-04-12/ID_HS_OrderLevel/2025-04-12_ID_HS_OrderLevel_exportdate_2025-07-09.csv"

exifPath="exiftool" #mac or linux
if(platform.system()=='Windows'):
    exifPath="exiftool-13.32_64/exiftool"
RANK_ORDER = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
# ──────────────────────────────────────────────────────────────────────────────


class ExifToolSession:
    def __init__(self, exiftool_path=exifPath):
        self.process = subprocess.Popen(
            [exiftool_path, "-stay_open", "True", "-@", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self._stderr_lines = []
        threading.Thread(target=self._drain_stderr, daemon=True).start()

    def _drain_stderr(self):
        for line in self.process.stderr:
            self._stderr_lines.append(line.strip())

    def _read_all_tags(self, image_path: str) -> dict:
        try:
            result = subprocess.run(
                [exifPath, "-j", "-n", image_path],
                capture_output=True, text=True, check=True
            )
            data = json.loads(result.stdout)[0]
            return data
        except Exception as e:
            print(f"⚠️ Could not read EXIF from {image_path}: {e}")
            return {}

    def wipe_and_rewrite_taxa_only(self, image_path: str, taxa_list: list[str]) -> None:
        existing_tags = self._read_all_tags(image_path)

        # ── Clean & deduplicate taxa for iNaturalist format ──
        seen = set()
        clean_taxa = []
        for taxon in taxa_list:
            cleaned = re.sub(r"\s+\(\d+\)$", "", taxon.strip())
            if cleaned and cleaned not in seen:
                clean_taxa.append(cleaned)
                seen.add(cleaned)

        # ── Build exiftool args ──
        args = ["-all="]  # Start clean to avoid duplication

        # Restore previous non-taxonomic metadata (preserve GPS, camera, datetime, etc.)
        for tag, value in existing_tags.items():
            tag_lc = tag.lower()
            if any(kw in tag_lc for kw in ["subject", "keyword", "usercomment", "imagedescription"]):
                continue  # Skip old taxonomy tags
            if tag == "SourceFile":
                continue  # Skip source reference
            safe_value = str(value).replace("\n", " ").replace("\r", "")
            args.append(f"-{tag}={safe_value}")

        # Re-add cleaned taxonomy to XMP-dc:Subject & MicrosoftPhoto LastKeywordXMP
        for tag in clean_taxa:
            args += [
                f"-XMP-dc:Subject+={tag}",
                f"-XMP-MicrosoftPhoto:LastKeywordXMP+={tag}"
            ]

        # Attempt to recover DateTimeOriginal from filename if not already preserved
        filename = Path(image_path).name
        m = re.search(r"_(\d{4})_(\d{2})_(\d{2})__?(\d{2})_(\d{2})_(\d{2})", filename)
        if m:
            y, mon, d, h, mi, s = m.groups()
            ts = f"{y}:{mon}:{d} {h}:{mi}:{s}"
            if not any("DateTimeOriginal" in t for t in args):
                args.append(f"-DateTimeOriginal={ts}")
            if not any("CreateDate" in t for t in args):
                args.append(f"-CreateDate={ts}")
            if not any("ModifyDate" in t for t in args):
                args.append(f"-ModifyDate={ts}")

        # Final exiftool command block
        args += ["-overwrite_original", str(image_path), "-execute\n"]

        self.process.stdin.write("\n".join(args) + "\n")
        self.process.stdin.flush()

        # Wait for confirmation from exiftool
        while True:
            if self.process.stdout.readline().strip() == "{ready}":
                break

    def close(self):
        self.process.stdin.write("-stay_open\nFalse\n")
        self.process.stdin.flush()
        self.process.wait()


def extract_taxa(row: dict) -> list[str]:
    return [row[r].strip() for r in RANK_ORDER if row.get(r) and row[r].strip()]


def embed_taxa_from_csv(csv_path: str):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        session = ExifToolSession()

        for row in reader:
            img_path = row["filepath"]
            taxa = extract_taxa(row)

            if not Path(img_path).exists():
                print(f"⚠️ File not found: {img_path}")
                continue
            if not taxa:
                print(f"⚠️ No taxonomy: {img_path}")
                continue

            print(f"✅ Writing clean taxa: {', '.join(taxa)} → {img_path}")
            session.wipe_and_rewrite_taxa_only(img_path, taxa)

        session.close()


if __name__ == "__main__":
    embed_taxa_from_csv(CSV_PATH)
