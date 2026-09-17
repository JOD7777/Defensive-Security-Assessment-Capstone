# Scope, Authorization & Rules of Engagement

## Authorization statement

I authorize the assessment of the local application contained in this repository. The application is owned/created for this lab and is intended to run only on localhost.

## Scope

**In scope**
- `src/app.py`
- `src/app_fixed.py`
- Local HTTP requests to `127.0.0.1`
- Application configuration, authentication logic, input validation, dependencies, and logging

**Out of scope**
- Public IP addresses
- Third-party services
- EdVyro infrastructure
- Other students' systems
- Real accounts, credentials, tokens, or personal data
- Denial of service, persistence, phishing, malware, destructive payloads, or credential stuffing

## Method

- Manual source/configuration review
- Low-rate local functional/security tests
- Reproducible checks using synthetic inputs only
- Before/after retesting following remediation

## Evidence rules

- Never store real passwords or tokens.
- Use placeholders such as `TEST_PASSWORD`.
- Sanitize screenshots and logs.
- Record only the minimum evidence required to demonstrate the finding.

## Stop conditions

Stop immediately if a test leaves the written scope, touches non-lab systems, or could affect availability or real data.
