"""
Production-Ready Technology Detector & Design System Scanner (Python 3.12+).
CLI Entry Point & Async Worker Orchestrator.

Reads website names and URLs from:
  - Markdown (.md) — default: government_ux4g_website_urls.md
  - Excel (.xlsx / .xls)
  - CSV (.csv)
  - PDF (.pdf)

Outputs: Excel, CSV, JSON reports + updates index.html dashboard.
Columns: Website, URL, Status, CSS Framework(s), Design System(s) Used,
         UX4G Design System (Yes/No), UX4G Accessibility CDN (Yes/No),
         Confidence, Evidence, Notes.
"""

from __future__ import annotations

import os
import re
import sys
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

# Force UTF-8 output on Windows terminals to avoid UnicodeEncodeError
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from config import (
    DEFAULT_MD_PATH,
    DEFAULT_EXCEL_INPUT_PATH,
    DEFAULT_PDF_PATH,
    DEFAULT_REPORTS_DIR,
    DEFAULT_INDEX_HTML,
    CONCURRENCY,
    REQUEST_TIMEOUT,
    USER_AGENT,
    REPORT_COLUMNS,
)
from crawler import CrawlerEngine
from detector import TechnologyDetector
from reporter import ReportExporter


# ─────────────────────────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────────────────────────

def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


# ─────────────────────────────────────────────────────────────────────────────
# Input Parsers
# ─────────────────────────────────────────────────────────────────────────────

def parse_md_file(path: str) -> list[dict[str, Any]]:
    """
    Parse lines like:
      1. DigiLocker — https://www.digilocker.gov.in/ — LIVE
      10. NIRI — No working URL found — VERIFY / NO URL CONFIRMED
    Returns list of dicts with keys: sno, website, url, status, notes.
    """
    entries: list[dict[str, Any]] = []
    pattern = re.compile(
        r"^(\d+)\.\s*(.*?)\s*[—–\-]+\s*(https?://[^\s—–]+|No working URL found|Not applicable|N/A)"
        r"(?:\s*[—–\-]+\s*(.*))?$",
        re.IGNORECASE,
    )

    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            m = pattern.match(line)
            if m:
                sno = int(m.group(1))
                name = m.group(2).strip()
                url_raw = m.group(3).strip()
                status_raw = (m.group(4) or "").strip()
                url = url_raw if url_raw.startswith("http") else None
                entries.append(
                    {
                        "sno": sno,
                        "website": name,
                        "url": url,
                        "status": status_raw or "UNKNOWN",
                        "notes": status_raw or "",
                    }
                )

    return entries


def parse_excel_file(path: str) -> list[dict[str, Any]]:
    import pandas as pd

    df = pd.read_excel(path)
    entries: list[dict[str, Any]] = []
    for idx, row in df.iterrows():
        website = str(row.get("Website", row.get("website", f"Project {idx + 1}"))).strip()
        url_raw = str(row.get("URL", row.get("url", ""))).strip()
        url = url_raw if url_raw.startswith("http") else None
        status = str(row.get("Status", row.get("status", ""))).strip() or "UNKNOWN"
        notes = str(row.get("Notes", row.get("notes", ""))).strip()
        entries.append(
            {
                "sno": idx + 1,
                "website": website,
                "url": url,
                "status": status,
                "notes": notes,
            }
        )
    return entries


def parse_csv_file(path: str) -> list[dict[str, Any]]:
    import pandas as pd

    df = pd.read_csv(path)
    entries: list[dict[str, Any]] = []
    for idx, row in df.iterrows():
        website = str(row.get("Website", row.get("website", f"Project {idx + 1}"))).strip()
        url_raw = str(row.get("URL", row.get("url", ""))).strip()
        url = url_raw if url_raw.startswith("http") else None
        status = str(row.get("Status", row.get("status", ""))).strip() or "UNKNOWN"
        notes = str(row.get("Notes", row.get("notes", ""))).strip()
        entries.append(
            {
                "sno": idx + 1,
                "website": website,
                "url": url,
                "status": status,
                "notes": notes,
            }
        )
    return entries


def load_entries_from_source(source_path: str) -> list[dict[str, Any]]:
    """Dispatch to the correct parser based on file extension."""
    ext = os.path.splitext(source_path)[1].lower()

    if ext == ".md":
        return parse_md_file(source_path)
    elif ext in (".xlsx", ".xls"):
        return parse_excel_file(source_path)
    elif ext == ".csv":
        return parse_csv_file(source_path)
    elif ext == ".pdf":
        from pdf_parser import extract_pdf_data  # only import if needed

        return extract_pdf_data(source_path)
    else:
        raise ValueError(f"Unsupported input file format: {ext}")


# ─────────────────────────────────────────────────────────────────────────────
# Worker
# ─────────────────────────────────────────────────────────────────────────────

def process_portal(
    entry: dict[str, Any],
    crawler: CrawlerEngine,
    detector: TechnologyDetector,
) -> dict[str, Any]:
    name = entry.get("website", "Unknown")
    url = entry.get("url")
    source_status = entry.get("status", "")
    notes = entry.get("notes", "")

    if not url:
        return {
            "Website": name,
            "URL": "N/A",
            "Status": source_status or "NO URL",
            "CSS Framework(s)": "None Detected",
            "Design System(s) Used": "None Detected",
            "UX4G Design System (Yes/No)": "No",
            "UX4G Accessibility CDN (Yes/No)": "No",
            "Confidence": "N/A",
            "Evidence": f"Portal skipped: No official URL ({notes})",
            "Notes": notes,
        }

    logging.info(f"Scanning [{entry.get('sno', '?')}] {name} -> {url}")
    crawl_res = crawler.fetch(url)
    det_res = detector.analyze(crawl_res)

    # Derive crawl status
    if crawl_res.get("status") == "Failed":
        crawl_status = "ERROR"
    elif crawl_res.get("status") == "Skipped":
        crawl_status = "SKIPPED"
    else:
        crawl_status = source_status or "LIVE"

    return {
        "Website": name,
        "URL": url,
        "Status": crawl_status,
        "CSS Framework(s)": det_res["css_frameworks"],
        "Design System(s) Used": det_res["design_systems"],
        "UX4G Design System (Yes/No)": det_res["ux4g_ds"],
        "UX4G Accessibility CDN (Yes/No)": det_res["ux4g_acc"],
        "Confidence": det_res["confidence"],
        "Evidence": det_res["evidence"],
        "Notes": notes,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "UX4G Design System & CSS Framework Detector — "
            "reads from .md / .xlsx / .csv / .pdf"
        )
    )
    parser.add_argument(
        "--input", "-i",
        default=None,
        help="Path to input file (.md, .xlsx, .csv, .pdf). Default: government_ux4g_website_urls.md",
    )
    parser.add_argument("--excel", default=None, help="Shorthand: path to input Excel file")
    parser.add_argument("--pdf", default=DEFAULT_PDF_PATH, help="Path to input PDF (fallback)")
    parser.add_argument("--output-dir", default=DEFAULT_REPORTS_DIR, help="Directory to save reports")
    parser.add_argument("--concurrency", type=int, default=CONCURRENCY, help="Concurrent crawlers")
    parser.add_argument("--timeout", type=int, default=REQUEST_TIMEOUT, help="HTTP request timeout (s)")
    parser.add_argument("--disable-playwright", action="store_true", help="Disable Playwright fallback")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose debug logging")
    args = parser.parse_args()

    setup_logging(args.verbose)

    # Resolve input file: --input > --excel > default .md > fallback xlsx > pdf
    if args.input:
        input_file = args.input
    elif args.excel:
        input_file = args.excel
    elif os.path.exists(DEFAULT_MD_PATH):
        input_file = DEFAULT_MD_PATH
    elif os.path.exists(DEFAULT_EXCEL_INPUT_PATH):
        input_file = DEFAULT_EXCEL_INPUT_PATH
    else:
        input_file = DEFAULT_PDF_PATH

    print("=" * 72)
    print("  UX4G Design System & CSS Framework Detector  (Python 3.12+)")
    print("=" * 72)
    print(f"[*] Input source : {input_file}")

    if not os.path.exists(input_file):
        print(f"[!] Error: File not found: {input_file}")
        sys.exit(1)

    entries = load_entries_from_source(input_file)
    print(f"[+] Loaded {len(entries)} entries\n")

    crawler = CrawlerEngine(
        timeout=args.timeout,
        user_agent=USER_AGENT,
        enable_playwright=not args.disable_playwright,
    )
    detector = TechnologyDetector()
    exporter = ReportExporter(output_dir=args.output_dir)

    print(f"[*] Crawling with {args.concurrency} concurrent workers...")

    results: list[dict[str, Any] | None] = [None] * len(entries)

    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        future_to_idx = {
            executor.submit(process_portal, entry, crawler, detector): idx
            for idx, entry in enumerate(entries)
        }

        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            entry = entries[idx]
            try:
                results[idx] = future.result()
            except Exception as exc:
                logging.error(f"Error on {entry.get('website')}: {exc}")
                results[idx] = {
                    "Website": entry.get("website", "Unknown"),
                    "URL": entry.get("url", "N/A"),
                    "Status": "ERROR",
                    "CSS Framework(s)": "None Detected",
                    "Design System(s) Used": "None Detected",
                    "UX4G Design System (Yes/No)": "No",
                    "UX4G Accessibility CDN (Yes/No)": "No",
                    "Confidence": "N/A",
                    "Evidence": f"Worker exception: {exc!s}",
                    "Notes": entry.get("notes", ""),
                }

    clean_results = [r for r in results if r is not None]

    # ── Enforce canonical column order ───────────────────────────────────────
    ordered_results = [
        {col: row.get(col, "") for col in REPORT_COLUMNS}
        for row in clean_results
    ]

    print("\n" + "=" * 72)
    print("  Generating Reports")
    print("=" * 72)

    csv_path = exporter.export_csv(ordered_results)
    print(f"[+] CSV   -> {csv_path}")

    json_path = exporter.export_json(ordered_results)
    print(f"[+] JSON  -> {json_path}")

    excel_path = exporter.export_excel(ordered_results)
    print(f"[+] Excel -> {excel_path}")

    html_path = DEFAULT_INDEX_HTML
    exporter.update_index_html(ordered_results, html_path)
    print(f"[+] HTML  -> {html_path}")

    # ── Summary ───────────────────────────────────────────────────────────────
    total = len(ordered_results)
    ux4g_ds = sum(1 for r in ordered_results if r["UX4G Design System (Yes/No)"] == "Yes")
    ux4g_acc = sum(1 for r in ordered_results if r["UX4G Accessibility CDN (Yes/No)"] == "Yes")
    high_conf = sum(1 for r in ordered_results if r["Confidence"] == "High")
    errors = sum(1 for r in ordered_results if r["Status"] == "ERROR")

    print("\n" + "-" * 72)
    print(f"  Total portals analysed      : {total}")
    print(f"  UX4G Design System (Yes)    : {ux4g_ds}  ({ux4g_ds / total * 100:.1f}%)")
    print(f"  UX4G Accessibility CDN (Yes): {ux4g_acc}  ({ux4g_acc / total * 100:.1f}%)")
    print(f"  High Confidence results     : {high_conf}")
    print(f"  Errors / unreachable        : {errors}")
    print("-" * 72)
    print("  Scan complete!\n")


if __name__ == "__main__":
    main()
