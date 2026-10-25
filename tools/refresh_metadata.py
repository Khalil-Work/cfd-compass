"""Read public GitHub metadata. Never execute or clone listed software."""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
GH = os.environ.get("GH_EXE", "gh")


def query(repo):
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        request = urllib.request.Request("https://api.github.com/repos/" + repo,
            headers={"Authorization": "Bearer " + token, "Accept": "application/vnd.github+json", "User-Agent": "CFD-Compass-metadata-audit"})
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.load(response)
    else:
        data = json.loads(subprocess.check_output([GH, "api", "repos/" + repo], text=True, encoding="utf-8"))
    return {field: data.get(field) for field in ["full_name", "html_url", "description", "private", "archived", "fork", "stargazers_count", "forks_count", "language", "created_at", "pushed_at", "updated_at", "default_branch"]} | {"license": (data.get("license") or {}).get("spdx_id", "NOASSERTION")}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=ROOT / "data/catalogue.json")
    parser.add_argument("--output", type=Path, default=ROOT / "data/metadata.json")
    args = parser.parse_args()
    entries = json.loads(args.input.read_text(encoding="utf-8"))
    with ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(query, [e["repo"] for e in entries]))
    seen = set()
    for entry, record in zip(entries, results):
        entry["repo"] = record["full_name"]
        key = record["full_name"].casefold()
        if key in seen:
            raise ValueError("Two entries resolve to the same upstream: " + key)
        seen.add(key)
    args.input.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    payload = {"checked_at": datetime.now(timezone.utc).isoformat(), "method": "GitHub REST repository metadata; project descriptions separately reviewed against primary sources", "repositories": {r["full_name"].casefold(): r for r in results}}
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Checked {len(results)} public upstream repositories; no source code downloaded.")


if __name__ == "__main__":
    main()
