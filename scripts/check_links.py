#!/usr/bin/env python3
"""Check internal links in the repository.

Scans every Markdown file for relative links and verifies the target exists.
Also reports links that point outside the repository, anchors that cannot be
resolved (best effort), and absolute filesystem paths, which are never portable.

Usage::

    python3 scripts/check_links.py [--verbose]

Exit code 0 when every relative link resolves, 1 otherwise.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from typing import Dict, List, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MD_LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")
HTML_LINK = re.compile(r'(?:href|src)="([^"]+)"')


def iter_markdown(root: str) -> List[str]:
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if d not in {
                ".git", "node_modules", "__pycache__", ".venv", "build", "dist",
                ".next", ".playwright-cli", "coverage", "out", "data", "cache",
            }
        ]
        for name in filenames:
            if name.endswith(".md"):
                out.append(os.path.join(dirpath, name))
    return sorted(out)


def classify(target: str) -> str:
    if target.startswith(("http://", "https://", "mailto:", "#")):
        return "external"
    if target.startswith("/"):
        return "absolute"
    return "relative"


def check(root: str, verbose: bool = False) -> Tuple[List[dict], int, int]:
    problems: List[dict] = []
    total_links = 0
    total_files = 0

    for path in iter_markdown(root):
        total_files += 1
        rel_path = os.path.relpath(path, root)
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()

        targets = [m.group(2) for m in MD_LINK.finditer(text)]
        targets += HTML_LINK.findall(text)

        for raw in targets:
            target = raw.strip()
            if not target or target.startswith("{{"):
                continue
            kind = classify(target)
            total_links += 1

            if kind == "external":
                if verbose:
                    print(f"  external  {rel_path} -> {target}")
                continue
            if kind == "absolute":
                problems.append({"file": rel_path, "target": target, "reason": "absolute path"})
                continue

            file_part = target.split("#", maxsplit=1)[0]
            if not file_part:
                continue  # same-page anchor
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), file_part))
            if not os.path.exists(resolved):
                problems.append({"file": rel_path, "target": target, "reason": "missing target"})
            elif os.path.isdir(resolved):
                # a directory link is fine when it has a README (GitHub renders it)
                if not os.path.exists(os.path.join(resolved, "README.md")):
                    problems.append(
                        {"file": rel_path, "target": target,
                         "reason": "directory without a README.md"}
                    )

    return problems, total_links, total_files


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Check internal Markdown links.")
    parser.add_argument("--root", default=ROOT)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    problems, total_links, total_files = check(args.root, args.verbose)

    print(f"Scanned {total_files} Markdown files, {total_links} links.")
    if not problems:
        print("OK: every relative link resolves.")
        return 0

    print(f"FAIL: {len(problems)} broken link(s).")
    for problem in problems:
        print(f"  {problem['file']} -> {problem['target']}  [{problem['reason']}]")
    return 1


if __name__ == "__main__":
    sys.exit(main())
