"""
Configuration module for Crawler and Report generation.
Python 3.12+ Production Configuration.
"""

import os

# Default Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PDF_PATH = os.path.join(BASE_DIR, "DIC and NEGD Projects With Links.pdf")
DEFAULT_MD_PATH = os.path.join(BASE_DIR, "government_ux4g_website_urls.md")
DEFAULT_EXCEL_INPUT_PATH = os.path.join(BASE_DIR, "websites_input.xlsx")
DEFAULT_REPORTS_DIR = os.path.join(BASE_DIR, "reports")
DEFAULT_INDEX_HTML = os.path.join(BASE_DIR, "index.html")

# Network & Crawler Settings
REQUEST_TIMEOUT = 18
PLAYWRIGHT_TIMEOUT = 30000  # 30 seconds in ms
CONCURRENCY = 6
MAX_RETRIES = 2
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

# Report Column Order (10 columns)
REPORT_COLUMNS = [
    "Website",
    "URL",
    "Status",
    "CSS Framework(s)",
    "Design System(s) Used",
    "UX4G Design System (Yes/No)",
    "UX4G Accessibility CDN (Yes/No)",
    "Confidence",
    "Evidence",
    "Notes",
]

# Confidence thresholds
CONFIDENCE_HIGH_THRESHOLD = 3
CONFIDENCE_MEDIUM_THRESHOLD = 1
