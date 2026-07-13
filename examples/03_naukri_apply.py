"""
03_naukri_apply.py — Apply to N jobs on a job board.

This is a PATTERN. It shows:
  - Open the search results page
  - Wait for jobs to actually load (not just for a fixed sleep)
  - Click each job, fill the form, submit
  - Save a record of what was applied to

⚠️ Read before running:
  - REPLACE <YOUR_CHROME_PROFILE_PATH> with your profile
  - REPLACE the SEARCH_URL with your actual job search
  - Adjust MAX_APPLICATIONS to a safe number
  - Most sites have rate limiting; pace your submissions
  - The exact selectors below are for one specific site. Adapt for yours.

Run:
  python examples/03_naukri_apply.py
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.session import browser_session
from core.resilience import smart_wait, react_aware_type


def main():
    PROFILE_PATH = "<YOUR_CHROME_PROFILE_PATH>"
    SEARCH_URL = "<JOB_SEARCH_URL>"  # e.g. https://example.com/jobs?q=power+bi
    MAX_APPLICATIONS = 5
    OUTPUT_FILE = "applications_log.json"

    if any(s.startswith("<YOUR_") or s.startswith("<JOB_")
           for s in [PROFILE_PATH, SEARCH_URL]):
        print("❌ Please edit the file and fill in PROFILE_PATH and SEARCH_URL.")
        sys.exit(1)

    applications = []

    with browser_session(profile_path=PROFILE_PATH) as (send, recv):
        # 1. Open search results
        print(f"→ Opening {SEARCH_URL}...")
        send({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
              "params": {"name": "browser_navigate",
                         "arguments": {"url": SEARCH_URL}}})
        recv()

        # 2. Wait for jobs to actually load
        print("→ Waiting for job listings...")
        # ⬇ adjust this selector to match your target site
        JOB_LIST_SELECTOR = "[data-job-id], .job-card, .job-listing"
        if not smart_wait(send, recv, "selector_present",
                          selector=JOB_LIST_SELECTOR, timeout=20):
            print("  ✗ No jobs loaded.")
            return
        print("  ✓ Jobs visible")

        # 3. Apply to the first N jobs
        for i in range(1, MAX_APPLICATIONS + 1):
            print(f"\n[Job {i}/{MAX_APPLICATIONS}]")
            time.sleep(3)  # be polite — pace your requests

            # Open the i-th job
            send({"jsonrpc": "2.0", "id": 10 + i, "method": "tools/call",
                  "params": {"name": "browser_evaluate",
                             "arguments": {
                                 "function": f"() => {{ const list = document.querySelectorAll('{JOB_LIST_SELECTOR}'); if (list[{i-1}]) {{ list[{i-1}].click(); return true; }} return false; }}"
                             }}})
            resp = recv(10)
            if not resp or "result" not in resp:
                print(f"  ✗ Could not open job {i}")
                continue
            time.sleep(2)

            # Click "Apply" — adapt selector
            send({"jsonrpc": "2.0", "id": 20 + i, "method": "tools/call",
                  "params": {"name": "browser_click",
                             "arguments": {"element": "Apply button",
                                           "ref": "button:has-text('Apply')"}}})
            recv(10)

            # If a form appears, fill the name field
            smart_wait(send, recv, "selector_present",
                       selector="input[name='name'], input#name",
                       timeout=5)
            react_aware_type(send, recv,
                             "input[name='name'], input#name",
                             "<YOUR FULL NAME>")

            # Click the final Submit
            send({"jsonrpc": "2.0", "id": 30 + i, "method": "tools/call",
                  "params": {"name": "browser_click",
                             "arguments": {"element": "Submit button",
                                           "ref": "button[type='submit']"}}})
            recv(10)

            applications.append({"job_index": i, "status": "applied"})
            print(f"  ✓ Applied to job {i}")

            # Go back to the search results
            send({"jsonrpc": "2.0", "id": 40 + i, "method": "tools/call",
                  "params": {"name": "browser_navigate_back",
                             "arguments": {}}})
            recv(5)
            smart_wait(send, recv, "selector_present",
                       selector=JOB_LIST_SELECTOR, timeout=10)

    # Save log
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(applications, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Done. Applied to {len(applications)} jobs. Log: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
