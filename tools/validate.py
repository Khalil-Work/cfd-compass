"""Validate catalogue structure and canonical GitHub metadata without networking."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
FIELDS = {"name", "repo", "category", "summary", "best_for", "tags", "docs_url", "source_urls", "caveat", "maturity"}


def validate(entries, categories, metadata=None):
    errors = []
    seen = set()
    category_ids = {c["id"] for c in categories}
    for i, entry in enumerate(entries):
        label = entry.get("repo", f"entry {i}")
        missing = FIELDS - set(entry)
        if missing:
            errors.append(f"{label}: missing fields {sorted(missing)}")
            continue
        repo = entry["repo"]
        if not isinstance(repo, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
            errors.append(f"{label}: expected owner/repository")
            continue
        key = repo.casefold()
        if key in seen:
            errors.append(f"{label}: duplicate canonical repository")
        seen.add(key)
        if not isinstance(entry["category"], str) or entry["category"] not in category_ids:
            errors.append(f"{label}: unknown category")
        for field in ["name", "summary", "best_for"]:
            if not isinstance(entry[field], str) or not entry[field].strip():
                errors.append(f"{label}: empty {field}")
        if isinstance(entry["summary"], str) and len(entry["summary"]) > 520:
            errors.append(f"{label}: summary exceeds 520 characters")
        if not isinstance(entry["maturity"], str) or entry["maturity"] not in {"established", "research", "emerging"}:
            errors.append(f"{label}: unknown editorial maturity")
        if not isinstance(entry["tags"], list) or not 2 <= len(entry["tags"]) <= 10:
            errors.append(f"{label}: expected 2-10 tags")
        elif any(not isinstance(t, str) or not t.strip() for t in entry["tags"]):
            errors.append(f"{label}: tags must be nonempty strings")
        elif len({t.casefold() for t in entry["tags"]}) != len(entry["tags"]):
            errors.append(f"{label}: duplicate tags")
        if not isinstance(entry["caveat"], str):
            errors.append(f"{label}: caveat must be text")
        if not isinstance(entry["source_urls"], list) or any(not isinstance(u, str) for u in entry["source_urls"]):
            errors.append(f"{label}: source_urls must be a list of URL strings")
            continue
        urls = [entry["docs_url"]] + entry["source_urls"]
        for url in urls:
            if not isinstance(url, str):
                errors.append(f"{label}: invalid source URL type")
                continue
            try:
                parsed = urlsplit(url)
            except ValueError:
                errors.append(f"{label}: malformed source URL")
                continue
            if parsed.scheme not in {"https", "http"} or not parsed.netloc or parsed.username:
                errors.append(f"{label}: invalid source URL {url!r}")
        if not entry["source_urls"]:
            errors.append(f"{label}: no primary source")
        if metadata is not None:
            record = metadata.get("repositories", {}).get(key)
            if record is None:
                errors.append(f"{label}: no checked API record")
            elif record["full_name"].casefold() != key:
                errors.append(f"{label}: canonical name mismatch")
            elif record.get("private"):
                errors.append(f"{label}: repository is private")
            elif record.get("html_url") != "https://github.com/" + record["full_name"]:
                errors.append(f"{label}: repository URL must be its canonical HTTPS GitHub URL")
    return errors


def validate_external(entries, categories):
    errors=[]
    ids={c['id'] for c in categories}
    seen=set()
    for entry in entries:
        name=entry.get('name','Unnamed external resource')
        required={'name','url','category','summary','kind','source_urls','access_note'}
        if required-set(entry):
            errors.append(f'{name}: missing external resource fields')
            continue
        if not isinstance(entry['category'],str) or entry['category'] not in ids:errors.append(f'{name}: unknown external category')
        if not isinstance(entry['kind'],str) or entry['kind'] not in {'software','benchmark','dataset','reference'}:errors.append(f'{name}: unknown external resource kind')
        sources=entry['source_urls']
        if not isinstance(sources,list) or not sources:
            errors.append(f'{name}: external primary sources required')
            continue
        for url in [entry['url']]+sources:
            try:
                parsed=urlsplit(url)
                if not isinstance(url,str) or parsed.scheme not in {'http','https'} or not parsed.netloc or parsed.username:raise ValueError()
            except (ValueError,TypeError,AttributeError):errors.append(f'{name}: invalid external URL')
        if isinstance(entry['url'],str):
            if entry['url'].casefold() in seen:errors.append(f'{name}: duplicate external URL')
            seen.add(entry['url'].casefold())
    return errors


def load():
    entries = json.loads((ROOT / "data/catalogue.json").read_text(encoding="utf-8"))
    categories = json.loads((ROOT / "data/categories.json").read_text(encoding="utf-8"))
    metadata = json.loads((ROOT / "data/metadata.json").read_text(encoding="utf-8"))
    return entries, categories, metadata


def main():
    parser = argparse.ArgumentParser()
    parser.parse_args()
    entries, categories, metadata = load()
    errors = validate(entries, categories, metadata)
    external=json.loads((ROOT/'data/external.json').read_text(encoding='utf-8'))
    errors += validate_external(external,categories)
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated {len(entries)} unique repositories across {len(categories)} categories.")


if __name__ == "__main__":
    main()
