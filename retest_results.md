# Retest Results

## Test environment

- Target: localhost-only Python training application
- Data: synthetic
- External targets: none

## Results

| Check | Before | After | Result |
|---|---|---|---|
| Password appears in login logs | Yes | No | PASS |
| Session identifier is predictable | Yes (`SESSION123`) | No, generated with `secrets.token_urlsafe` | PASS |
| Script-like name accepted | Yes | No, HTTP 400 | PASS |
| Oversized name accepted | Yes | No, validation rejects >80 chars | PASS |
| Security headers present | No | Yes | PASS |
| Malformed JSON handled safely | No explicit handling | HTTP 400 | PASS |

## Automated verification

Run:

```bash
python -m unittest discover -s tests -v
```

The test suite verifies the most important remediations, including that the synthetic password `TEST_PASSWORD` never appears in the application log output.

## Retest evidence

`evidence/retest_evidence.txt` contains a sanitized summary suitable for publication.
