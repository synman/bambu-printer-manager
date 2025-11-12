WIP — Linting & Issue Templates setup

This draft PR adds a standardized Python linting and formatting toolchain plus repository issue templates to help with triage. The changes are intentionally non-functional (formatting & tooling) and are targeted at the `devel` branch so we can stage these repo-wide improvements before merging to `main`.

Summary of changes
- Add formatting/linters and pre-commit:
  - Black and isort configuration merged into pyproject.toml
  - .pre-commit-config.yaml to run Black, isort, Flake8, Pylint, and common pre-commit hooks
  - requirements-dev.txt with developer dependencies
  - Makefile with helper targets (lint, lint-fix, format, precommit-install)
  - .flake8 and .pylintrc for Flake8/Pylint settings
- CI enforcement:
  - .github/workflows/lint.yml to run Black/isort/Flake8, optional Pylint, and pre-commit on push/PR for devel/main/linting-* branches
- Repository hygiene:
  - .gitignore preserved and enhanced with common Python/project entries
- Issue templates:
  - .github/ISSUE_TEMPLATE/bug_report.md
  - .github/ISSUE_TEMPLATE/feature_request.md
  - .github/ISSUE_TEMPLATE/config.yml (disables blank issues and adds a Discussions contact link)

PR statistics (current)
- Commits: 14
- Files changed: 13
- Additions: 284
- Deletions: 1

Checklist
- [x] Black and isort configured in pyproject.toml
- [x] Flake8 and Pylint config files included
- [x] pre-commit configured
- [x] CI workflow added to run lint checks
- [x] requirements-dev.txt added
- [x] Issue templates (bug report, feature request) added
- [x] ISSUE_TEMPLATE config.yml added (blank_issues_enabled: false + support link)

Examples
- Concrete example files were added to the branch:
  - Bug report example: https://github.com/synman/bambu-printer-manager/blob/add-issue-templates/.github/ISSUE_TEMPLATE/examples/bug_report_example.md
  - Feature request example: https://github.com/synman/bambu-printer-manager/blob/add-issue-templates/.github/ISSUE_TEMPLATE/examples/feature_request_example.md

  Short excerpt (from the bug report example):
  > **Summary**  
  > When attempting to connect to my Bambu X1C, the manager fails with a connection timeout after ~10 seconds.
  >
  > **Steps to reproduce**  
  > 1. Install the manager from the `main` branch.  
  > 2. Start the manager and click "Add printer".  
  > 3. Enter the printer IP address `192.168.1.42` and click Connect.

Notes for reviewers
- Pylint is included but intentionally not blocking in CI (marked optional) because it can be noisy. If you prefer stricter enforcement, we can change the workflow to fail the job on Pylint errors.
- Black and isort target settings live in pyproject.toml — update target-version or line-length there if you want different formatting rules.
- The pre-commit hooks will auto-fix many issues locally; please run the local checks before merging so we don't apply automatic formatting in a separate commit later.
- Issue templates are simple and focused; we can add front-matter (labels, assignees) to auto-apply labels if you want automated triage.

How to validate locally (quick)
1. Checkout the branch:
   git checkout linting-setup
2. Create & activate a venv:
   python -m venv .venv && source .venv/bin/activate
3. Install dev deps:
   python -m pip install --upgrade pip
   python -m pip install -r requirements-dev.txt
4. Install pre-commit hooks & run all hooks:
   pre-commit install
   pre-commit run --all-files
5. Run tool checks:
   black --check .
   isort --check-only .
   flake8 .
   # optional: pylint src/ || true

Suggested follow-ups (separate PRs)
- Run Black/isort autofix across the repository (if you want formatting changes applied in this PR, we can add them; otherwise keep lint-only for review).
- Optionally run Pylint progressively or add per-module pylintrc overrides if specific modules need different rules.
- Add GitHub issue/PR templates that auto-apply labels or projects (I can add label front-matter if you want).