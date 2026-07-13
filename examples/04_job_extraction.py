"""
04_job_extraction.py — Extract a list of jobs from a search results page.

What it does:
  1. Opens a job search page
  2. Waits for the listings to actually load
  3. Pulls title, company, location, link from each card
  4. Saves to a JSON file

This is a PATTERN. The selectors below are examples. Adjust them to
match the site you're scraping.

Run:
  python examples/04_job_extraction.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.session import browser_session
from core.resilience import smart_wait


def main():
    PROFILE_PATH = "<YOUR_CHROME_PROFILE_PATH>"
    SEARCH_URL = "<JOB_SEARCH_URL>"
    OUTPUT_FILE = "extracted_jobs.json"

    if any(s.startswith("<YOUR_") or s.startswith("<JOB_")
           for s in [PROFILE_PATH, SEARCH_URL]):
        print("❌ Please edit PROFILE_PATH and SEARCH_URL.")
        sys.exit(1)

    with browser_session(profile_path=PROFILE_PATH) as (send, recv):
        print(f"→ Opening {SEARCH_URL}...")
        send({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
              "params": {"name": "browser_navigate",
                         "arguments": {"url": SEARCH_URL}}})
        recv()

        # Wait for listings
        JOB_CARD_SELECTOR = "<JOB_CARD_CSS_SELECTOR>"  # e.g. ".job-listing"
        if not smart_wait(send, recv, "selector_present",
                          selector=JOB_CARD_SELECTOR, timeout=20):
            print("  ✗ No listings appeared.")
            return

        # Extract via JS evaluate
        # The selector templates below are placeholders — adjust to your site
        extract_js = """
        () => {
            const cards = document.querySelectorAll('<JOB_CARD_CSS_SELECTOR>');
            const out = [];
            cards.forEach(card => {
                out.push({
                    title:    (card.querySelector('<TITLE_SELECTOR>')    || {}).innerText || '',
                    company:  (card.querySelector('<COMPANY_SELECTOR>')  || {}).innerText || '',
                    location: (card.querySelector('<LOCATION_SELECTOR>') || {}).innerText || '',
                    link:     (card.querySelector('a') || {}).href || '',
                });
            });
            return JSON.stringify(out);
        }
        """

        print("→ Extracting...")
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
              "params": {"name": "browser_evaluate",
                         "arguments": {"function": extract_js}}})
        resp = recv(15)
        if not resp or "result" not in resp:
            print("  ✗ Extraction failed.")
            return

        content = resp["result"].get("content", [])
        raw = content[0].get("text", "") if content else ""
        try:
            jobs = json.loads(raw)
        except json.JSONDecodeError:
            print(f"  ✗ Could not parse response. Raw: {raw[:300]}")
            return

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)

        print(f"✓ Extracted {len(jobs)} jobs to {OUTPUT_FILE}")
        for j in jobs[:3]:
            print(f"  - {j.get('title','?')} @ {j.get('company','?')}")


if __name__ == "__main__":
    main()
