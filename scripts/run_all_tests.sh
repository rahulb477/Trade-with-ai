#!/usr/bin/env bash
# Run the full verification suite.
#
#   ./scripts/run_all_tests.sh
#
# Steps: unit tests -> link check -> repository audit. Stops on the first failure.

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

status=0
step() { printf '\n\033[1m== %s ==\033[0m\n' "$1"; }

step "1/3  Unit tests"
if ! python3 -m unittest discover -s tests -t . ; then
  echo "unit tests FAILED"
  status=1
fi

step "2/3  Internal links"
if ! python3 scripts/check_links.py; then
  echo "link check FAILED"
  status=1
fi

step "3/3  Repository audit"
if ! python3 scripts/audit_repo.py; then
  echo "audit FAILED"
  status=1
fi

step "Summary"
if [ "$status" -eq 0 ]; then
  echo "ALL CHECKS PASSED"
else
  echo "ONE OR MORE CHECKS FAILED"
fi
exit "$status"
