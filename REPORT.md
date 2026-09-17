# Defensive Security Assessment Report

## Executive summary

A controlled assessment was performed against a deliberately local training application. The review covered configuration, authentication/session handling, input validation, dependency hygiene, and logging. Three reproducible weaknesses were identified in the initial implementation. The highest-risk issues were remediated and retested using synthetic data.

No external systems, real credentials, personal data, or public services were targeted.

## Scope and authorization

See `scope_and_roE.md`. The application is bound to `127.0.0.1` and is intended for isolated local testing only.

## Methodology

- Source/configuration inspection
- Local functional testing
- Negative input testing
- Log inspection
- Dependency review
- Before/after retesting

## Findings

| ID | Finding | Severity | Evidence | Remediation |
|---|---|---|---|---|
| SEC-01 | Password exposed in application logs | High | Initial login handler logged the password field | Removed password from logs; retained username and outcome only |
| SEC-02 | Predictable/static session identifier | High | Initial login returned `SESSION123` | Generate cryptographically random session token and set `HttpOnly; SameSite=Strict` cookie |
| SEC-03 | Missing input validation | Medium | Profile endpoint accepted script-like and oversized names | Length, character, JSON and body-size validation added |
| SEC-04 | Missing baseline response hardening | Low | Initial responses lacked common defensive headers | Added `X-Content-Type-Options`, restrictive CSP and `Cache-Control: no-store` |

## Reproducibility

### SEC-01

1. Start the initial application.
2. Submit a synthetic login using `student / TEST_PASSWORD`.
3. Inspect stdout/log output.
4. Initial implementation prints the password value.

Expected after remediation: logs contain only a username and success/failure result.

### SEC-02

1. Submit a successful synthetic login.
2. Inspect the response.
3. Initial implementation returns the constant `SESSION123`.
4. Remediated implementation returns no token in JSON and places a random token in an `HttpOnly; SameSite=Strict` cookie.

### SEC-03

1. Send a profile request containing `<script>alert(1)</script>`.
2. Initial implementation accepts the value.
3. Remediated implementation returns HTTP 400.
4. Names over 80 characters are also rejected.

## Risk rationale

- Logging credentials can expose reusable authentication material through local log files or centralized log collection.
- Predictable session identifiers can permit session guessing/fixation-style abuse if other controls are weak.
- Missing validation increases the chance of injection, malformed-data handling, and resource-abuse issues.
- Missing security headers reduce browser-side defense-in-depth.

## Remediation summary

The remediated version:
- removes password logging;
- generates random session tokens with Python `secrets`;
- sets safer cookie attributes;
- validates input type, length, and allowed characters;
- rejects oversized request bodies;
- handles malformed JSON;
- adds baseline response headers.

## Retest conclusion

All defined remediation checks pass in the local test suite. See `retest_results.md` and `tests/test_security.py`.

## Evidence handling

All examples use synthetic values. No real secrets or personal information are included.
