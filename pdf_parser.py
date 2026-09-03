"""
PDF Extractor module to accurately parse project names, URLs, ministries, statuses, and notes from PDF files.
"""

import re
import pypdf
import pdfplumber
from typing import List, Dict, Any


def extract_pdf_data(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Extracts structured website list from the PDF document.
    Handles coordinate-based hyperlink extraction and text alignment.
    """
    reader = pypdf.PdfReader(pdf_path)
    page0_pdf = reader.pages[0]
    annots = page0_pdf.get('/Annots', [])
    
    hyperlinks = []
    for a in annots:
        obj = a.get_object()
        if '/A' in obj and '/URI' in obj['/A']:
            uri = obj['/A']['/URI']
            if uri != 'http://s.no/':
                rect = [float(x) for x in obj['/Rect']]
                y_mid = (rect[1] + rect[3]) / 2.0
                hyperlinks.append({'uri': uri, 'rect': rect, 'y': y_mid})

    # Sort hyperlinks from top to bottom
    hyperlinks.sort(key=lambda item: -item['y'])

    # Standard clean name fixes for line-overflowed PDF entries
    name_cleanups = {
        11: 'NSWS (National Single Window System)',
        13: 'DPE (Department of Public Enterprises)',
        14: 'ITPO - Bharat Mandapam',
        15: 'IPA (Indian Ports Association)',
        16: 'BRICS (India 2026 Digital Platform)',
        17: 'Portal Consolidation - Social Justice (DoSJE Unified Portal)',
        19: 'Gaming Portal (Online Gaming Authority of India)',
        21: 'MOTA / Survey App (Ministry of Tribal Affairs)',
        24: 'UPMS (Unified Project Management System)',
        27: 'Niti for States - NFS',
        31: 'RR Generator - DoPT',
        33: 'AI Chatbots (MeitY Parliamentary Qs, NMC, NSWS, etc.)',
        42: 'Election Commission of India - IIDEM',
        44: 'ABC / NAD (Academic Bank of Credits)',
        54: 'GSI (Geological Survey of India)',
        58: 'DPDP Digital Office (Data Protection Board of India)',
        59: 'NCW (National Commission for Women)',
        60: 'Vandemataram (150 Years of Vande Mataram)'
    }

    results = []
    with pdfplumber.open(pdf_path) as pdf:
        table = pdf.pages[0].extract_table()
        rows = table[1:] if table else []

    link_idx = 0
    for idx, row in enumerate(rows):
        sno = int(row[0]) if row[0] and row[0].strip().isdigit() else (idx + 1)
        raw_name = row[1].strip() if row[1] else f"Project {sno}"
        raw_url_col = row[2].strip() if len(row) > 2 and row[2] else ''
        ministry = row[3].strip() if len(row) > 3 and row[3] else ''
        status = row[4].strip() if len(row) > 4 and row[4] else ''
        notes = row[5].strip() if len(row) > 5 and row[5] else ''

        if sno in [10, 20, 33]:
            url = None
        else:
            if link_idx < len(hyperlinks):
                url = hyperlinks[link_idx]['uri']
                link_idx += 1
            else:
                # Regex fallback
                m = re.search(r'https?://[^\s\)]+', raw_url_col)
                url = m.group(0) if m else None

        clean_name = name_cleanups.get(sno, raw_name.replace('\ufffd', '-').strip())

        results.append({
            'sno': sno,
            'website': clean_name,
            'url': url,
            'ministry': ministry,
            'pdf_status': status,
            'notes': notes
        })

    return results
