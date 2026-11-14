"""Repository-integrity tests.

These tests treat the documentation as a deliverable with a contract: links must
resolve, required files must exist, and forbidden patterns must not appear.
"""

import os
import re
import unittest

from tests import REPO_ROOT
from tests.support import FLAT  # noqa: F401  (ensures sys.path is set up)

import sys
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))

import check_links  # noqa: E402
import audit_repo   # noqa: E402

VERDICTS = [
    "BULLISH SCENARIO",
    "BEARISH SCENARIO",
    "WAIT — NO CONFIRMED SETUP",
    "NO-TRADE",
    "INSUFFICIENT DATA — NO VALID SETUP",
]


def read(rel_path):
    with open(os.path.join(REPO_ROOT, rel_path), "r", encoding="utf-8") as handle:
        return handle.read()


class TestLinks(unittest.TestCase):
    def test_all_relative_links_resolve(self):
        problems, links, files = check_links.check(REPO_ROOT)
        self.assertGreater(files, 150, "unexpectedly few Markdown files")
        self.assertGreater(links, 300, "unexpectedly few links")
        if problems:
            detail = "\n".join(f"{p['file']} -> {p['target']} [{p['reason']}]" for p in problems)
            self.fail(f"{len(problems)} broken link(s):\n{detail}")


class TestRequiredStructure(unittest.TestCase):
    def test_required_items_exist(self):
        self.assertEqual(audit_repo.check_required(REPO_ROOT), [])

    def test_knowledge_directories_have_readmes(self):
        self.assertEqual(audit_repo.check_knowledge_readmes(REPO_ROOT), [])

    def test_no_third_party_imports(self):
        self.assertEqual(audit_repo.check_imports(REPO_ROOT), [])

    def test_no_empty_or_tiny_markdown(self):
        self.assertEqual(audit_repo.check_markdown(REPO_ROOT), [])

    def test_no_placeholder_markers(self):
        issues = audit_repo.scan_patterns(REPO_ROOT, audit_repo.PLACEHOLDER_PATTERNS, "placeholder")
        self.assertEqual(issues, [])

    def test_no_fabrication_language(self):
        issues = audit_repo.scan_patterns(
            REPO_ROOT, audit_repo.FABRICATION_PATTERNS, "fabrication"
        )
        self.assertEqual(issues, [])

    def test_no_credential_shaped_strings(self):
        issues = audit_repo.scan_patterns(
            REPO_ROOT, audit_repo.CREDENTIAL_PATTERNS, "credential"
        )
        self.assertEqual(issues, [])


class TestVocabulary(unittest.TestCase):
    def test_skill_defines_every_verdict(self):
        text = read("SKILL.md")
        for verdict in VERDICTS:
            self.assertIn(verdict, text, f"SKILL.md is missing the verdict: {verdict}")

    def test_templates_use_the_closed_vocabulary(self):
        text = read("templates/analysis-report.md")
        for verdict in VERDICTS:
            self.assertIn(verdict, text)

    def test_no_free_text_verdict_markers(self):
        for rel_path in ("templates/analysis-report.md", "templates/paper-trade-report.md"):
            text = read(rel_path).lower()
            self.assertNotIn("verdict: probably", text)

    def test_decision_engine_documents_the_gate_ladder(self):
        text = read("core/decision-engine.md")
        for gate in ("G1", "G4", "G5", "G7"):
            self.assertIn(gate, text)


class TestSafetyStatements(unittest.TestCase):
    def test_root_docs_disclaim_advice(self):
        for rel_path in ("README.md", "SKILL.md", "AGENTS.md"):
            text = read(rel_path).lower()
            self.assertIn("advice", text, f"{rel_path} must state the no-advice position")

    def test_no_execution_claims(self):
        for rel_path in ("README.md", "SKILL.md", "AGENTS.md"):
            text = read(rel_path).lower()
            self.assertIn("broker", text, f"{rel_path} must address broker integration")
            prohibitions = [line for line in text.splitlines() if "broker" in line]
            self.assertTrue(
                any(
                    any(word in line for word in ("never", "no ", "not ", "out of scope"))
                    for line in prohibitions
                ),
                f"{rel_path} mentions a broker without prohibiting it",
            )

    def test_limitations_document_exists_and_is_specific(self):
        text = read("docs/limitations.md")
        self.assertGreater(len(text), 4000)
        self.assertIn("cannot make you profitable", text.lower())


class TestKnowledgeConsistency(unittest.TestCase):
    def test_indicator_files_match_implemented_functions(self):
        implemented = {
            "sma", "ema", "rsi", "macd", "atr", "adx", "bollinger-bands", "supertrend",
            "stochastic-rsi", "obv", "vwap", "ichimoku-cloud", "cci", "roc", "mfi",
            "pivot-points", "fibonacci", "volume-profile",
        }
        directory = os.path.join(REPO_ROOT, "knowledge", "indicators")
        present = {name[:-3] for name in os.listdir(directory) if name.endswith(".md")}
        missing = implemented - present
        self.assertEqual(missing, set(), f"documented but not implemented: {missing}")

    def test_pattern_detectors_are_documented(self):
        text = read("integrations/python/trading_intel/patterns.py")
        detectors = set(re.findall(r"^def detect_([a-z_]+)\(", text, re.MULTILINE))
        detectors.discard("all")  # detect_all() is the aggregate runner, not a pattern
        # every detector must be registered in DETECTORS
        registry = read("integrations/python/trading_intel/patterns.py")
        for name in detectors:
            self.assertIn(f'"{name}"', registry, f"detector {name} is not registered")

    def test_glossary_covers_newer_domains(self):
        text = read("knowledge/glossary.md").lower()
        for term in ("order block", "fair value gap", "wilson", "monte carlo", "circuit breaker"):
            self.assertIn(term, text)


if __name__ == "__main__":
    unittest.main()
