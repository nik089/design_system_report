"""
Evidence-Based Technology Detection Engine (Python 3.12+).

Enforces strict separation between:
  - UX4G Design System  (UI components, CDN CSS, ux4g-* DOM classes, --ux4g-* CSS vars)
  - UX4G Accessibility CDN  (accessibility-widget.js / accessibility.ux4g.gov.in)

Confidence scoring:
  High   ≥ 3 evidence points  OR  UX4G DS / UX4G Acc confirmed
  Medium  1-2 evidence points
  Low    0 evidence points  OR  crawl failed / skipped
"""

from __future__ import annotations

import re
from typing import Any

from tech_signatures import CSS_FRAMEWORKS, DESIGN_SYSTEMS


class TechnologyDetector:
    def __init__(self) -> None:
        self.frameworks = CSS_FRAMEWORKS
        self.design_systems = DESIGN_SYSTEMS

    # ─────────────────────────────────────────────────────────────────────────
    # Public entry point
    # ─────────────────────────────────────────────────────────────────────────

    def analyze(self, crawl_data: dict[str, Any]) -> dict[str, Any]:
        """
        Returns:
            css_frameworks       – comma-separated string or "None Detected"
            design_systems       – comma-separated string or "Custom / None Detected"
            ux4g_ds              – "Yes" | "No"
            ux4g_acc             – "Yes" | "No"
            confidence           – "High" | "Medium" | "Low" | "N/A"
            evidence             – detailed pipe-separated string
        """
        status = crawl_data.get("status", "")
        if status in ("Skipped", "Failed"):
            err = crawl_data.get("error", "Website unreachable")
            return {
                "css_frameworks": "None Detected",
                "design_systems": "None Detected",
                "ux4g_ds": "No",
                "ux4g_acc": "No",
                "confidence": "N/A",
                "evidence": f"Portal skipped or unreachable: {err}",
            }

        html: str = crawl_data.get("html", "")
        css_urls: list[str] = crawl_data.get("css_urls", [])
        js_urls: list[str] = crawl_data.get("js_urls", [])
        css_content: str = crawl_data.get("css_content", "")
        dom_classes: set[str] = crawl_data.get("dom_classes", set())
        dom_attrs: set[str] = crawl_data.get("dom_attrs", set())
        meta_tags: list[str] = crawl_data.get("meta_tags", [])

        all_asset_urls = css_urls + js_urls
        full_text = html + "\n" + css_content  # used for inline/raw pattern checks

        # ── UX4G Accessibility CDN ────────────────────────────────────────────
        has_ux4g_acc, ux4g_acc_evidence = self._detect_ux4g_acc(
            all_asset_urls, full_text
        )

        # ── UX4G Design System ────────────────────────────────────────────────
        has_ux4g_ds, ux4g_ds_evidence = self._detect_ux4g_ds(
            css_urls, all_asset_urls, dom_classes, css_content, meta_tags, full_text
        )

        # ── CSS Frameworks ────────────────────────────────────────────────────
        detected_frameworks: list[str] = []
        framework_evidence: list[str] = []

        for name, sig in self.frameworks.items():
            matched, details = self._match_signature(
                sig, all_asset_urls, css_content, dom_classes, dom_attrs, full_text,
                class_threshold=2
            )
            if matched:
                detected_frameworks.append(name)
                framework_evidence.append(f"{name} ({'; '.join(details)})")

        # ── Design Systems / UI Libraries ─────────────────────────────────────
        detected_ds: list[str] = []
        ds_evidence: list[str] = []

        if has_ux4g_ds:
            detected_ds.append("UX4G Design System")
            ds_evidence.append(f"UX4G Design System ({', '.join(ux4g_ds_evidence)})")

        for name, sig in self.design_systems.items():
            if name in ("UX4G Design System", "UX4G Accessibility CDN"):
                continue
            matched, details = self._match_signature(
                sig, all_asset_urls, css_content, dom_classes, dom_attrs, full_text,
                class_threshold=1
            )
            if matched:
                detected_ds.append(name)
                ds_evidence.append(f"{name} ({'; '.join(details)})")

        # ── Build output strings ──────────────────────────────────────────────
        fw_text = ", ".join(detected_frameworks) if detected_frameworks else "None Detected"
        ds_text = ", ".join(detected_ds) if detected_ds else "Custom / None Detected"

        evidence_parts: list[str] = []
        confidence_points = 0

        if has_ux4g_ds:
            evidence_parts.append(f"[UX4G DS]: {', '.join(ux4g_ds_evidence)}")
            confidence_points += 4

        if has_ux4g_acc:
            evidence_parts.append(f"[UX4G Accessibility CDN]: {', '.join(ux4g_acc_evidence)}")
            confidence_points += 2

        if framework_evidence:
            evidence_parts.append(f"[Frameworks]: {'; '.join(framework_evidence)}")
            confidence_points += len(detected_frameworks) * 2

        if ds_evidence:
            evidence_parts.append(f"[UI Libraries]: {'; '.join(ds_evidence)}")
            confidence_points += len(detected_ds) * 2

        if not evidence_parts:
            evidence_str = (
                f"HTML analysed ({len(html):,} bytes), "
                f"{len(css_urls)} CSS files, "
                f"{len(js_urls)} JS scripts — "
                "no standard framework signatures matched."
            )
            confidence = "Low"
        else:
            evidence_str = " | ".join(evidence_parts)
            if confidence_points >= 3 or has_ux4g_ds or has_ux4g_acc:
                confidence = "High"
            elif confidence_points >= 1:
                confidence = "Medium"
            else:
                confidence = "Low"

        return {
            "css_frameworks": fw_text,
            "design_systems": ds_text,
            "ux4g_ds": "Yes" if has_ux4g_ds else "No",
            "ux4g_acc": "Yes" if has_ux4g_acc else "No",
            "confidence": confidence,
            "evidence": evidence_str,
        }

    # ─────────────────────────────────────────────────────────────────────────
    # UX4G-specific detectors
    # ─────────────────────────────────────────────────────────────────────────

    def _detect_ux4g_acc(
        self, all_asset_urls: list[str], full_text: str
    ) -> tuple[bool, list[str]]:
        sig = self.design_systems.get("UX4G Accessibility CDN", {})
        evidence: list[str] = []

        for url in all_asset_urls:
            for pat in sig.get("cdn_patterns", []):
                if re.search(pat, url, re.IGNORECASE):
                    evidence.append(f"CDN/File: {url}")
                    return True, evidence

        for pat in sig.get("cdn_patterns", []):
            if re.search(pat, full_text, re.IGNORECASE):
                evidence.append(f"Inline: {pat}")
                return True, evidence

        return False, evidence

    def _detect_ux4g_ds(
        self,
        css_urls: list[str],
        all_asset_urls: list[str],
        dom_classes: set[str],
        css_content: str,
        meta_tags: list[str],
        full_text: str,
    ) -> tuple[bool, list[str]]:
        sig = self.design_systems.get("UX4G Design System", {})
        evidence: list[str] = []
        detected = False

        # CDN / CSS links
        for url in css_urls:
            for pat in sig.get("cdn_patterns", []):
                if re.search(pat, url, re.IGNORECASE):
                    detected = True
                    evidence.append(f"CDN/File: {url}")
                    break

        # DOM classes starting with ux4g-
        ux4g_classes = sorted({c for c in dom_classes if c.lower().startswith("ux4g-")})
        if ux4g_classes:
            detected = True
            evidence.append(f"Classes: [{', '.join(ux4g_classes[:6])}]")

        # CSS custom properties
        if re.search(r"--ux4g-", css_content, re.IGNORECASE):
            detected = True
            evidence.append("CSS Var: --ux4g-*")

        # Meta tags
        for meta in meta_tags:
            if "ux4g" in meta.lower():
                detected = True
                evidence.append(f"Meta: {meta[:80]}")

        # Raw HTML inline patterns (e.g. script loading ux4g CSS)
        if not detected:
            for pat in sig.get("cdn_patterns", []):
                if re.search(pat, full_text, re.IGNORECASE):
                    detected = True
                    evidence.append(f"Inline: {pat}")
                    break

        return detected, evidence

    # ─────────────────────────────────────────────────────────────────────────
    # Generic signature matcher
    # ─────────────────────────────────────────────────────────────────────────

    def _match_signature(
        self,
        sig: dict[str, Any],
        all_asset_urls: list[str],
        css_content: str,
        dom_classes: set[str],
        dom_attrs: set[str],
        full_text: str,
        class_threshold: int = 2,
    ) -> tuple[bool, list[str]]:
        """
        Returns (matched: bool, evidence_details: list[str]).
        class_threshold: minimum number of matching class patterns required
                         when classes are the only evidence source.
        """
        details: list[str] = []
        matched = False

        # 1. CDN / asset URL patterns
        for url in all_asset_urls:
            for pat in sig.get("cdn_patterns", []):
                if re.search(pat, url, re.IGNORECASE):
                    fname = url.split("/")[-1].split("?")[0]
                    details.append(f"CDN/File: {fname}")
                    matched = True
                    break
            if matched:
                break

        # 2. CSS variable patterns
        for pat in sig.get("var_patterns", []):
            if re.search(pat, css_content, re.IGNORECASE | re.MULTILINE):
                details.append(f"CSS Var: {pat.lstrip('^')[:40]}")
                matched = True
                break

        # 3. DOM attribute patterns
        for attr_str in dom_attrs:
            for pat in sig.get("attr_patterns", []):
                if re.search(pat, attr_str, re.IGNORECASE):
                    details.append(f"Attr: {pat[:40]}")
                    matched = True
                    break
            if matched:
                break

        # 4. DOM class patterns
        matched_classes: list[str] = []
        for pat in sig.get("class_patterns", []):
            for cls in dom_classes:
                if re.search(pat, cls, re.IGNORECASE):
                    if cls not in matched_classes:
                        matched_classes.append(cls)
                    if len(matched_classes) >= 6:
                        break
            if len(matched_classes) >= 6:
                break

        sufficient_classes = len(matched_classes) >= class_threshold
        if sufficient_classes or (matched_classes and matched):
            if matched_classes:
                details.append(f"Classes: [{', '.join(matched_classes[:4])}]")
            matched = True

        # 5. Raw HTML inline meta patterns
        for pat in sig.get("meta_patterns", []):
            if re.search(pat, full_text, re.IGNORECASE):
                details.append(f"Meta: {pat[:40]}")
                matched = True
                break

        return matched, details
