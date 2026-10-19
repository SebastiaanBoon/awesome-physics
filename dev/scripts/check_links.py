#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""Check every URL in README.md using only the Python standard library.

Usage:
    python3 dev/scripts/check_links.py --concurrency 16 --timeout 15

Statuses:
    ok      - HTTP 2xx
    warn    - HTTP 403, 405, 429, or a non-fatal redirect problem
    broken  - HTTP 4xx/5xx other than the above, or a connection error

Exit code is 1 when at least one link is broken, 0 otherwise.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import pathlib
import re
import ssl
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
README = ROOT / "README.md"

URL_RE = re.compile(r"\]\((https?://[^)\s]+)\)")

USER_AGENT = (
    "Mozilla/5.0 (compatible; awesome-physics-link-checker/1.0; "
    "+https://github.com/awesome-physics)"
)

WARN_CODES = {401, 403, 405, 406, 429}


def extract_urls(path: pathlib.Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    seen: dict[str, None] = {}
    for match in URL_RE.finditer(text):
        url = match.group(1).rstrip(".,;")
        seen.setdefault(url, None)
    return list(seen)


def make_request(url: str) -> urllib.request.Request:
    return urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
        },
        method="GET",
    )


def check(url: str, timeout: float) -> tuple[str, str, str]:
    context = ssl.create_default_context()
    try:
        with urllib.request.urlopen(make_request(url), timeout=timeout, context=context) as response:
            return url, "ok", str(response.status)
    except urllib.error.HTTPError as error:
        if error.code in WARN_CODES:
            return url, "warn", str(error.code)
        return url, "broken", str(error.code)
    except urllib.error.URLError as error:
        return url, "broken", f"URLError: {error.reason}"
    except TimeoutError:
        return url, "broken", "timeout"
    except (ssl.SSLError, OSError) as error:
        return url, "broken", type(error).__name__


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readme", default=str(README))
    parser.add_argument("--concurrency", type=int, default=12)
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument("--report", default="", help="Optional path for a full report.")
    args = parser.parse_args()

    urls = extract_urls(pathlib.Path(args.readme))
    print(f"Checking {len(urls)} unique URLs with concurrency {args.concurrency}...\n")

    results: list[tuple[str, str, str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = {pool.submit(check, url, args.timeout): url for url in urls}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda item: (item[1], item[0]))
    counts = {"ok": 0, "warn": 0, "broken": 0}
    for url, status, detail in results:
        counts[status] += 1
        if status != "ok":
            print(f"[{status}] {url} ({detail})")

    print(f"\nok: {counts['ok']}  warn: {counts['warn']}  broken: {counts['broken']}")

    if args.report:
        lines = [f"{status}\t{detail}\t{url}" for url, status, detail in results]
        pathlib.Path(args.report).write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Report written to {args.report}")

    return 1 if counts["broken"] else 0


if __name__ == "__main__":
    sys.exit(main())
