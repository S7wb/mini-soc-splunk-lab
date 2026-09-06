#!/usr/bin/env python3
"""Check local repository structure. Does not execute SPL or contact the lab."""

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit


def without_fences(text):
    lines = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return "\n".join(lines)


def anchors(text):
    found = set(re.findall(r'\b(?:id|name)=[\"\']([^\"\']+)', text))
    counts = Counter()
    for title in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", without_fences(text), re.M):
        title = re.sub(r"!?\[([^]]+)\]\([^)]*\)", r"\1", title)
        title = re.sub(r"<[^>]*>", "", title).lower()
        slug = re.sub(r"[^\w\-\s]", "", title).replace(" ", "-")
        count = counts[slug]
        counts[slug] += 1
        found.add(slug if count == 0 else f"{slug}-{count}")
    return found


def validate(root):
    errors = []
    checked_links = 0
    files = sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.relative_to(root).parts)
    for path in files:
        relative = path.relative_to(root)
        if path.suffix == ".md":
            body = without_fences(path.read_text(encoding="utf-8"))
            targets = re.findall(r"!?\[[^\]\n]*\]\(([^\n)]+)\)", body)
            targets += re.findall(r'^\s*\[[^\]]+\]:\s*(\S+)', body, re.M)
            targets += re.findall(r'\b(?:src|href)=[\"\']([^\"\']+)', body)
            for raw in targets:
                target = raw.split(' "', 1)[0].strip("<>")
                uri = urlsplit(target)
                if uri.scheme or uri.netloc:
                    continue
                destination = (root / unquote(uri.path).lstrip("/") if uri.path.startswith("/")
                               else path.parent / unquote(uri.path)) if uri.path else path
                destination = destination.resolve()
                checked_links += 1
                if not destination.is_relative_to(root):
                    errors.append(f"{relative}: link escapes repository: {target}")
                elif not destination.exists():
                    errors.append(f"{relative}: missing link: {target}")
                elif uri.fragment and destination.is_file() and destination.suffix == ".md":
                    if unquote(uri.fragment) not in anchors(destination.read_text(encoding="utf-8")):
                        errors.append(f"{relative}: missing anchor: {target}")
        elif path.suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (ValueError, UnicodeError) as exc:
                errors.append(f"{relative}: invalid JSON: {exc}")
        elif path.suffix == ".png":
            if path.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
                errors.append(f"{relative}: invalid PNG signature")
        elif path.suffix == ".spl" and not path.read_text(encoding="utf-8").strip():
            errors.append(f"{relative}: empty SPL file")

    roadmap = root / "use-cases/README.md"
    if not roadmap.is_file():
        errors.append("Missing use-cases/README.md")
        roadmap_ids = []
    else:
        roadmap_ids = [int(n) for n in re.findall(r"^\| UC-(\d{2}) \|", roadmap.read_text(encoding="utf-8"), re.M)]
    packages = sorted(p for p in (root / "use-cases").glob("phase-*/uc-*") if p.is_dir())
    package_ids = [int(p.name.split("-")[1]) for p in packages]
    if Counter(roadmap_ids) != Counter(package_ids):
        errors.append("Roadmap IDs and package IDs differ or a package is missing")
    if any(count != 1 for count in Counter(package_ids).values()):
        errors.append("Duplicate use-case ID")
    for phase in (root / "use-cases").glob("phase-*"):
        if phase.is_dir() and not (phase / "README.md").is_file():
            errors.append(f"{phase.relative_to(root)}: missing phase index")
    for package in packages:
        for name in ("README.md", "alert-configuration.md", "incident-report.md", "evidence/README.md"):
            if not (package / name).is_file():
                errors.append(f"{package.relative_to(root)}: missing {name}")
        readme = package / "README.md"
        if readme.exists() and "**Status:** Planned" in readme.read_text(encoding="utf-8"):
            if (package / "detection.spl").exists():
                errors.append(f"{package.relative_to(root)}: update Planned status when SPL development begins")

    for path in root.rglob("privileged_accounts.csv"):
        with path.open(newline="", encoding="utf-8") as handle:
            header = next(csv.reader(handle), [])
        if header != ["user", "account_type", "severity"]:
            errors.append(f"{path.relative_to(root)}: unexpected lookup columns")

    return errors, {"files": len(files), "local_links": checked_links, "use_cases": len(packages)}


def main():
    root = Path(__file__).resolve().parents[1]
    errors, counts = validate(root)
    for error in errors:
        print("ERROR:", error)
    print(json.dumps({"ok": not errors, **counts, "errors": len(errors)}, indent=2))
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
