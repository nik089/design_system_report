"""
High-Performance Crawler Engine with Requests + BeautifulSoup and Playwright Fallback.
"""

import re
import urllib3
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Dict, Any, List, Set, Optional

# Disable insecure HTTPS warnings for robust scanning of public portals
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger("Crawler")


class CrawlerEngine:
    def __init__(self, timeout: int = 18, user_agent: str = None, enable_playwright: bool = True):
        self.timeout = timeout
        self.user_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        self.enable_playwright = enable_playwright
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
            "Upgrade-Insecure-Requests": "1"
        })

    def fetch(self, url: str) -> Dict[str, Any]:
        """
        Fetches the website homepage, extracts HTML, linked CSS files, JS scripts, meta tags, and inline styles.
        Falls back to Playwright if needed (e.g., SPA, 403, or JS required).
        """
        if not url or url.lower() in ["none", "n/a", "not applicable", "not confirmed"]:
            return {
                "status": "Skipped",
                "final_url": url,
                "html": "",
                "css_urls": [],
                "js_urls": [],
                "css_content": "",
                "dom_classes": set(),
                "dom_attrs": set(),
                "meta_tags": [],
                "error": "No official website URL in PDF entry"
            }

        # Step 1: Attempt HTTP request via requests
        try:
            resp = self.session.get(url, timeout=self.timeout, verify=False, allow_redirects=True)
            if resp.status_code == 200 and len(resp.text) > 400:
                return self._parse_html_response(resp.url, resp.text)
            elif self.enable_playwright:
                logger.info(f"Requests returned status {resp.status_code} for {url}. Attempting Playwright fallback...")
                return self._fetch_playwright(url)
            else:
                return self._parse_html_response(resp.url, resp.text, error=f"HTTP {resp.status_code}")
        except Exception as e:
            if self.enable_playwright:
                logger.info(f"Requests failed for {url} ({e}). Attempting Playwright fallback...")
                return self._fetch_playwright(url)
            return {
                "status": "Failed",
                "final_url": url,
                "html": "",
                "css_urls": [],
                "js_urls": [],
                "css_content": "",
                "dom_classes": set(),
                "dom_attrs": set(),
                "meta_tags": [],
                "error": str(e)
            }

    def _fetch_playwright(self, url: str) -> Dict[str, Any]:
        """
        Headless Playwright Chromium fetcher for dynamic / SPA / protected portals.
        """
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent=self.user_agent,
                    ignore_https_errors=True,
                    viewport={"width": 1280, "height": 800}
                )
                page = context.new_page()
                page.set_default_timeout(25000)
                
                try:
                    response = page.goto(url, wait_until="domcontentloaded", timeout=25000)
                except Exception:
                    # Retry with commit wait
                    response = page.goto(url, wait_until="commit", timeout=20000)
                    page.wait_for_timeout(2000)

                final_url = page.url
                html = page.content()
                browser.close()
                return self._parse_html_response(final_url, html)
        except Exception as e:
            return {
                "status": "Failed",
                "final_url": url,
                "html": "",
                "css_urls": [],
                "js_urls": [],
                "css_content": "",
                "dom_classes": set(),
                "dom_attrs": set(),
                "meta_tags": [],
                "error": f"Playwright error: {str(e)[:150]}"
            }

    def _parse_html_response(self, base_url: str, html: str, error: Optional[str] = None) -> Dict[str, Any]:
        soup = BeautifulSoup(html, "html.parser")
        
        # Extract CSS links
        css_urls = []
        for link in soup.find_all("link", rel=lambda r: r and "stylesheet" in r):
            href = link.get("href")
            if href:
                css_urls.append(urljoin(base_url, href))

        # Extract JS scripts
        js_urls = []
        for script in soup.find_all("script", src=True):
            src = script.get("src")
            if src:
                js_urls.append(urljoin(base_url, src))

        # Extract DOM classes
        dom_classes: Set[str] = set()
        for el in soup.find_all(class_=True):
            classes = el.get("class", [])
            if isinstance(classes, list):
                dom_classes.update(classes)
            elif isinstance(classes, str):
                dom_classes.update(classes.split())

        # Extract DOM Attributes & Names
        dom_attrs: Set[str] = set()
        for el in soup.find_all(True):
            for attr in el.attrs:
                val = el.attrs[attr]
                if isinstance(val, str):
                    dom_attrs.add(f"{attr}={val}")
                dom_attrs.add(attr)
            if el.name:
                dom_attrs.add(f"<{el.name}")

        # Meta tags
        meta_tags = []
        for meta in soup.find_all("meta"):
            content = meta.get("content", "")
            name = meta.get("name", meta.get("property", ""))
            if content:
                meta_tags.append(f"{name}:{content}")

        # Fetch first few key CSS files to check for variables
        css_sample_content = ""
        for css_url in css_urls[:4]:
            try:
                css_resp = self.session.get(css_url, timeout=5, verify=False)
                if css_resp.status_code == 200:
                    css_sample_content += "\n" + css_resp.text[:50000]
            except Exception:
                pass

        # Inline style tags
        for style_tag in soup.find_all("style"):
            css_sample_content += "\n" + style_tag.get_text()

        return {
            "status": "Active" if not error else "Warning",
            "final_url": base_url,
            "html": html,
            "css_urls": css_urls,
            "js_urls": js_urls,
            "css_content": css_sample_content,
            "dom_classes": dom_classes,
            "dom_attrs": dom_attrs,
            "meta_tags": meta_tags,
            "error": error
        }
