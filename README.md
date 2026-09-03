# Production-Ready Design System & CSS Framework Detector (Python 3.12+)

A high-performance, multi-layered Python 3.12+ application that reads website names and URLs from a PDF document, crawls each homepage using **Requests + BeautifulSoup** with automatic **Playwright Headless Chromium** fallback for JavaScript-rendered single page applications (SPAs), and performs deep technology detection across HTML, linked CSS files, JavaScript, DOM elements, meta tags, and CDNs.

---

## Key Features

- **Automated PDF Parsing**: Extracts website names, URLs, ministries, statuses, and notes from structured PDF tables and hyperlinked PDF annotations (using `pdfplumber` + `pypdf`).
- **Hybrid Web Crawler Engine**:
  - **Requests + BeautifulSoup**: Super-fast concurrent HTTP fetching with SSL bypass and desktop User-Agent spoofing.
  - **Playwright Fallback**: Automatically renders JavaScript-heavy websites, dynamic SPAs (React, Angular, Vue, Svelte), and bypasses WAF/Cloudflare/403 blocks.
- **Strict UX4G Verification**:
  - Detects **UX4G Design System (Yes/No)** via UX4G CSS files, `.ux4g-*` DOM class prefixes, `--ux4g-*` CSS variables, and UX4G meta tags.
  - Detects **UX4G Accessibility CDN (Yes/No)** via `accessibility-widget.js` and `accessibility.ux4g.gov.in`.
  - **Strict Separation Enforced**: The presence of the UX4G Accessibility CDN widget does **NOT** flag UX4G Design System as Yes unless actual UX4G Design System CSS/UI components are used.
- **17 CSS Frameworks Supported**:
  Bootstrap, Tailwind CSS, Bulma, Foundation, Semantic UI, Materialize CSS, UIkit, Pure CSS, Pico CSS, W3.CSS, Spectre.css, Milligram, Skeleton CSS, Tachyons, Halfmoon, UnoCSS, Windi CSS.
- **40 Design Systems & UI Libraries Supported**:
  UX4G Design System, Angular Material, Material UI (MUI), Ant Design, PrimeNG, PrimeReact, PrimeVue, Chakra UI, Mantine, Carbon Design System, Fluent UI, PatternFly, Salesforce Lightning Design System, Atlassian Design System, Adobe Spectrum, Shopify Polaris, SAP Fiori, Oracle Redwood, GOV.UK Design System, USWDS, Clarity, Base Web, Evergreen UI, Grommet, Blueprint.js, Elastic UI, Kendo UI, Syncfusion, DevExtreme, Nebular, Taiga UI, NG-ZORRO, Vuetify, Quasar, Element Plus, Shoelace, Radix UI, HeroUI, React Bootstrap, Custom Design Systems.
- **Professional Reports Generated**:
  Generates reports with exact requested columns:
  `Website`, `URL`, `CSS Framework(s)`, `Design System/UI Library Used`, `UX4G Design System (Yes/No)`, `UX4G Accessibility CDN (Yes/No)`, `Confidence`, `Evidence`
  - **Excel Workbook (`.xlsx`)**: With styled headers, zebra striping, auto column width, conditional formatting, and an Executive Summary dashboard sheet.
  - **CSV (`.csv`)**: Standard UTF-8 CSV report.
  - **Interactive HTML Dashboard (`.html`)**: Mobile-responsive Bootstrap dashboard with live search bar, status filter dropdowns, stat cards, and evidence modal boxes.
  - **JSON Dump (`.json`)**: Machine-readable JSON output.
  - **Rich Terminal Table**: Colorized summary table printed directly to stdout.

---

## Installation & Setup

1. Install Python 3.12 or 3.11+
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Playwright Chromium browser binary:
   ```bash
   python -m playwright install chromium
   ```

---

## Usage

### Run on Default PDF (`DIC and NEGD Projects With Links.pdf`):
```bash
python main.py
```

### Advanced CLI Options:
```bash
python main.py --pdf "path/to/your.pdf" --output-dir "./custom_reports" --concurrency 10 --timeout 20
```

### CLI Arguments Reference:
| Argument | Default | Description |
|---|---|---|
| `--pdf` | `DIC and NEGD Projects With Links.pdf` | Path to PDF file containing website links |
| `--output-dir` | `./reports` | Directory where output reports will be saved |
| `--concurrency` | `5` | Number of concurrent crawler workers |
| `--timeout` | `15` | HTTP request timeout in seconds |
| `--use-playwright-only` | `False` | Force Playwright headless browser for all URLs |
| `--disable-playwright` | `False` | Disable Playwright fallback (Requests only) |
| `--verbose` | `False` | Enable detailed debug logs |

---

## Output Report Structure

Every generated report contains the exact 8 columns:

1. **Website**: Name of the website or project/initiative extracted from PDF.
2. **URL**: Clean official website URL crawled.
3. **CSS Framework(s)**: Detected framework(s) (e.g., Bootstrap, Tailwind CSS, Bulma) or `None Detected`.
4. **Design System/UI Library Used**: Detected design system (e.g., UX4G Design System, Material UI, Angular Material) or `Custom / None Detected`.
5. **UX4G Design System (Yes/No)**: `Yes` if UX4G Design System CSS/UI component library is implemented; `No` otherwise.
6. **UX4G Accessibility CDN (Yes/No)**: `Yes` if UX4G Accessibility widget script is included; `No` otherwise.
7. **Confidence**: `High`, `Medium`, or `Low` based on match evidence strength.
8. **Evidence**: Detailed string listing matched CDNs, CSS files, DOM class patterns, CSS variables, or meta tags.

---

## Architecture Overview

```
.
├── main.py                     # Main CLI entry point & async task orchestrator
├── config.py                   # App configuration & timeout options
├── pdf_parser.py               # PDFExtractor reading tables and PDF hyperlink annotations
├── crawler.py                  # WebCrawler engine (Requests + Playwright Fallback)
├── tech_signatures.py          # Signature rules for 17 CSS Frameworks & 40 Design Systems
├── detector.py                 # TechnologyDetector evaluating match rules & confidence
├── reporter.py                 # ReportExporter producing Excel, CSV, HTML, JSON & CLI table
├── requirements.txt            # Dependency specs
└── README.md                   # Project documentation
```


``Build a production-ready Python 3.12+ application that reads website names and URLs from an Excel file, crawls each homepage (using Requests + BeautifulSoup, with Playwright fallback for JavaScript-rendered pages), and detects the CSS Framework(s) and Design System/UI Library used. Analyze HTML, linked CSS, JavaScript, meta tags, DOM, and external assets to identify technologies. Specifically verify whether the website implements the UX4G Design System and UX4G Accessibility CDN/Widget by detecting UX4G-specific classes, CSS variables, components, CDN links, and accessibility scripts. Detect CSS frameworks including Bootstrap, Tailwind CSS, Bulma, Foundation, Semantic UI, Materialize CSS, UIkit, Pure CSS, Pico CSS, W3.CSS, Spectre.css, Milligram, Skeleton CSS, Tachyons, Halfmoon, UnoCSS, and Windi CSS. Detect design systems and UI libraries including UX4G Design System, Angular Material, Material UI (MUI), Ant Design, PrimeNG, PrimeReact, PrimeVue, Chakra UI, Mantine, Carbon Design System, Fluent UI, PatternFly, Salesforce Lightning Design System, Atlassian Design System, Adobe Spectrum, Shopify Polaris, SAP Fiori, Oracle Redwood, GOV.UK Design System, USWDS, Clarity, Base Web, Evergreen UI, Grommet, Blueprint.js, Elastic UI, Kendo UI, Syncfusion, DevExtreme, Nebular, Taiga UI, NG-ZORRO, Vuetify, Quasar, Element Plus, Shoelace, Radix UI, HeroUI, React Bootstrap, and Custom Design Systems. Generate professional Excel, CSV, and JSON reports with columns: Website, URL, Status, CSS Framework(s), Design System(s) Used, UX4G Design System (Yes/No), UX4G Accessibility CDN (Yes/No), Confidence, Evidence, and Notes. Use evidence-based verification with High/Medium/Low confidence and include robust error handling, retries, logging, and concurrent scanning.``