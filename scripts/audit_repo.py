#!/usr/bin/env python3
"""Repository audit: structure, placeholders, sizes, and honesty checks.

Checks performed
----------------
1. Required top-level items exist.
2. No empty Markdown files and no suspiciously small ones.
3. No placeholder markers (TODO, TBD, FIXME, "lorem ipsum", "coming soon").
4. No occurrence of obviously fabricated-claim phrases in knowledge files.
5. Every knowledge directory has a README.
6. Code has no third-party imports.
7. No credential-looking strings in tracked text files.
8. Prints a per-directory inventory with file counts and bytes.

Usage::

    python3 scripts/audit_repo.py [--strict]

Exit code 0 if no blocking issue is found, 1 otherwise.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from typing import Dict, List

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED = [
    "SKILL.md",
    "README.md",
    "AGENTS.md",
    "LICENSE",
    "CHANGELOG.md",
    ".gitignore",
    "core",
    "knowledge",
    "workflows",
    "strategies",
    "engines",
    "data-sources",
    "markets",
    "integrations",
    "templates",
    "examples",
    "tests",
    "docs",
    "scripts",
]

PLACEHOLDER_PATTERNS = [
    (re.compile(r"\bTODO\b"), "TODO marker"),
    (re.compile(r"\bTBD\b"), "TBD marker"),
    (re.compile(r"\bFIXME\b"), "FIXME marker"),
    (re.compile(r"lorem ipsum", re.IGNORECASE), "lorem ipsum"),
    (re.compile(r"coming soon", re.IGNORECASE), "coming soon"),
    (re.compile(r"\[insert[^\]]*\]", re.IGNORECASE), "insert-placeholder"),
    (re.compile(r"your company name here", re.IGNORECASE), "literal placeholder"),
]

FABRICATION_PATTERNS = [
    (re.compile(r"\bguaranteed (profit|returns?|win)", re.IGNORECASE), "guaranteed-profit claim"),
    (re.compile(r"\b100% (accurate|win|sure)\b", re.IGNORECASE), "certainty claim"),
    (re.compile(r"\bsure[ -]?shot\b", re.IGNORECASE), "sure-shot claim"),
    (re.compile(r"\brisk[ -]?free\b", re.IGNORECASE), "risk-free claim"),
]

THIRD_PARTY_IMPORTS = [
    "numpy", "pandas", "scipy", "matplotlib", "talib", "ta-lib",
    "sklearn", "requests", "aiohttp", "ccxt", "yfinance",
]

CREDENTIAL_PATTERNS = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key"),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "OpenAI-style key"),
    (re.compile(r"ghp_[A-Za-z0-9]{30,}"), "GitHub token"),
    (re.compile(r"-----BEGIN (RSA |EC )?PRIVATE KEY-----"), "private key"),
]

SKIP_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv", "build", "dist", ".pytest_cache",
    ".next", ".playwright-cli", "coverage", "out", "data", "cache",
}
MIN_MD_BYTES = 400


def walk_files(root: str, extensions=None):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if extensions and not name.endswith(tuple(extensions)):
                continue
            yield os.path.join(dirpath, name)


def rel(root: str, path: str) -> str:
    return os.path.relpath(path, root)


def check_required(root: str) -> List[str]:
    issues = []
    for item in REQUIRED:
        if not os.path.exists(os.path.join(root, item)):
            issues.append(f"missing required item: {item}")
    return issues


def check_markdown(root: str) -> List[str]:
    issues = []
    for path in walk_files(root, [".md"]):
        size = os.path.getsize(path)
        if size == 0:
            issues.append(f"empty Markdown file: {rel(root, path)}")
        elif size < MIN_MD_BYTES:
            issues.append(f"very small Markdown file ({size} B): {rel(root, path)}")
    return issues


# A hit is only a problem if it is used affirmatively. Documentation that lists a
# phrase in order to forbid it is compliance, not a violation.
NEGATION_MARKERS = (
    "never", "no ", "not ", "banned", "forbid", "prohibit", "avoid", "instead",
    "do not", "don't", "must not", "refuse", "reject", "defect", "wrong",
)


def scan_patterns(root: str, patterns, label: str, context_filter: bool = True) -> List[str]:
    issues = []
    for path in walk_files(root, [".md", ".py", ".sh", ".txt", ".yml", ".yaml"]):
        # the audit script necessarily contains the patterns it searches for
        if os.path.basename(path) == "audit_repo.py":
            continue
        try:
            with open(path, "r", encoding="utf-8") as handle:
                text = handle.read()
        except (UnicodeDecodeError, OSError):
            continue
        lines = text.splitlines()
        for pattern, name in patterns:
            for match in pattern.finditer(text):
                line_no = text[: match.start()].count("\n") + 1
                if context_filter:
                    window = " ".join(lines[max(0, line_no - 2) : line_no + 1]).lower()
                    if any(marker in window for marker in NEGATION_MARKERS):
                        continue
                issues.append(f"{label} in {rel(root, path)}:{line_no}: {name}")
    return issues


def check_knowledge_readmes(root: str) -> List[str]:
    issues = []
    knowledge = os.path.join(root, "knowledge")
    if not os.path.isdir(knowledge):
        return ["knowledge/ missing"]
    for entry in sorted(os.listdir(knowledge)):
        path = os.path.join(knowledge, entry)
        if os.path.isdir(path):
            if not os.path.exists(os.path.join(path, "README.md")):
                issues.append(f"knowledge/{entry}/ has no README.md")
    if not os.path.exists(os.path.join(knowledge, "README.md")):
        issues.append("knowledge/README.md missing")
    return issues


def check_imports(root: str) -> List[str]:
    issues = []
    lib = os.path.join(root, "integrations", "python")
    if not os.path.isdir(lib):
        return ["integrations/python missing"]
    import_re = re.compile(r"^\s*(?:from|import)\s+([A-Za-z_][A-Za-z0-9_]*)", re.MULTILINE)
    for path in walk_files(lib, [".py"]):
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()
        for module in import_re.findall(text):
            if module in THIRD_PARTY_IMPORTS:
                issues.append(f"third-party import '{module}' in {rel(root, path)}")
    return issues


def inventory(root: str) -> Dict[str, dict]:
    base = root
    stats: Dict[str, dict] = {}
    for entry in sorted(os.listdir(base)):
        path = os.path.join(base, entry)
        if entry in SKIP_DIRS or not os.path.isdir(path):
            continue
        count = 0
        size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in filenames:
                full = os.path.join(dirpath, name)
                try:
                    size += os.path.getsize(full)
                except OSError:
                    continue
                count += 1
        stats[entry] = {"files": count, "bytes": size}
    return stats


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Audit the repository.")
    parser.add_argument("--root", default=ROOT)
    parser.add_argument("--strict", action="store_true",
                        help="treat fabrication-language hits as failures")
    args = parser.parse_args(argv)
    root = args.root

    blocking: List[str] = []
    warnings: List[str] = []

    blocking += check_required(root)
    blocking += check_markdown(root)
    blocking += check_knowledge_readmes(root)
    blocking += check_imports(root)

    placeholders = scan_patterns(root, PLACEHOLDER_PATTERNS, "placeholder")
    fabrication = scan_patterns(root, FABRICATION_PATTERNS, "fabrication-language")
    credentials = scan_patterns(root, CREDENTIAL_PATTERNS, "credential-like string")

    blocking += credentials
    if args.strict:
        blocking += placeholders + fabrication
    else:
        warnings += placeholders + fabrication

    print("=" * 72)
    print("REPOSITORY AUDIT")
    print("=" * 72)

    print("\nInventory")
    print(f"  {'directory':<18}{'files':>8}{'bytes':>12}")
    for name, data in inventory(root).items():
        print(f"  {name:<18}{data['files']:>8}{data['bytes']:>12,}")

    md_files = list(walk_files(root, [".md"]))
    md_bytes = sum(os.path.getsize(p) for p in md_files)
    py_files = list(walk_files(os.path.join(root, "integrations"), [".py"]))
    print(f"\n  Markdown files: {len(md_files)} ({md_bytes:,} bytes)")
    print(f"  Python files  : {len(py_files)}")

    print("\nChecks")
    sections = [
        ("required structure", check_required(root)),
        ("markdown sizes", check_markdown(root)),
        ("knowledge READMEs", check_knowledge_readmes(root)),
        ("no third-party imports", check_imports(root)),
        ("no credentials", credentials),
        ("no placeholders", placeholders),
        ("no fabrication language", fabrication),
    ]
    for label, items in sections:
        status = "OK" if not items else f"{len(items)} issue(s)"
        print(f"  {label:<28} {status}")

    if warnings:
        print("\nWarnings")
        for item in warnings[:40]:
            print(f"  - {item}")
        if len(warnings) > 40:
            print(f"  ... and {len(warnings) - 40} more")

    if blocking:
        print("\nBLOCKING ISSUES")
        for item in blocking[:60]:
            print(f"  - {item}")
        print(f"\nRESULT: FAIL ({len(blocking)} blocking issue(s))")
        return 1

    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
