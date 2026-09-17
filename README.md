# Defensive Security Assessment Capstone

A beginner-friendly, authorized defensive security assessment of a small local application.

## Scope

- Target: `src/app.py`
- Environment: localhost only
- Test window: local development/testing session
- Authorization: the application in this repository is intentionally created for this assessment.
- No external systems, public IPs, third-party accounts, real credentials, or personal data were used.

## Assessment areas

1. Configuration and security headers
2. Authentication and session handling
3. Input validation
4. Dependency hygiene
5. Logging and secret exposure

## Deliverables

- `REPORT.md` — sanitized assessment report
- `retest_results.md` — before/after verification
- `scope_and_roE.md` — authorization and rules of engagement
- `src/app.py` — local demonstration application
- `src/app_fixed.py` — remediated version
- `tests/test_security.py` — reproducible checks
- `evidence/` — sanitized evidence
- `assessment_report.pdf` — portfolio-ready report

## Run

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
python src/app.py
```

The demo binds to `127.0.0.1` only.

## Test

```bash
python -m unittest discover -s tests -v
```

The tests exercise the remediated controls and document the intended security properties.

## Safety

This repository is for an isolated local defensive lab. Do not point the code or tests at systems you do not own or lack explicit authorization to assess.
