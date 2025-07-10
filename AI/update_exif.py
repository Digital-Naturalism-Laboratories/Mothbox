import csv
import re
import subprocess
import threading
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────────────
CSV_PATH = "/Users/brianna/Desktop/Indonesia_Deployments/Les_DurianFarm_EfectoMinla_2025-07-04/2025-07-04/BriID/2025-07-04_BriID_exportdate_2025-07-10.csv"
EXIFTOOL_BIN = "exiftool"
RANK_ORDER = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
# ──────────────────────────────────────────────────────────────────────────────


class ExifToolSession:
    def __init__(self, exiftool_path=EXIFTOOL_BIN):
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

    def wipe_and_write_taxa(self, image_path: str, taxa_list: list[str]) -> None:
        args = []

        # ── Deduplicate and clean ──
        seen = set()
        clean_taxa = []
        for taxon in taxa_list:
            cleaned = re.sub(r"\s+\(\d+\)$", "", taxon.strip())
            if cleaned and cleaned not in seen:
                clean_taxa.append(cleaned)
                seen.add(cleaned)

        # ── First, remove ALL prior metadata ──
        args += ["-all="]

        # ── Add new cleaned keywords ──
        for tag in clean_taxa:
            args += [
                f"-XMP-dc:Subject+={tag}",
                f"-XMP-MicrosoftPhoto:LastKeywordXMP+={tag}",
                f"-MWG:Keywords+={tag}",
            ]

        # ── Set timestamp from filename ──
        filename = Path(image_path).name
        m = re.search(r"_(\d{4})_(\d{2})_(\d{2})__?(\d{2})_(\d{2})_(\d{2})", filename)
        if m:
            y, mon, d, h, mi, s = m.groups()
            ts = f"{y}:{mon}:{d} {h}:{mi}:{s}"
            args += [
                f"-DateTimeOriginal={ts}",
                f"-CreateDate={ts}",
                f"-ModifyDate={ts}"
            ]

        args += ["-overwrite_original", str(image_path), "-execute\n"]

        self.process.stdin.write("\n".join(args) + "\n")
        self.process.stdin.flush()

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

            print(f"✅ Updating tags: {', '.join(taxa)} → {img_path}")
            session.wipe_and_write_taxa(img_path, taxa)

        session.close()


if __name__ == "__main__":
    embed_taxa_from_csv(CSV_PATH)
