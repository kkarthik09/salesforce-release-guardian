# Salesforce Release Guardian

Dependency blast-radius analysis, test mapping and owner approval release gates.

Status: initial reference implementation, developed with substantial AI assistance.
No industry adoption, technical novelty, production readiness is claimed.
All sample data is synthetic. This project is independent of Salesforce and is not endorsed by Salesforce.

## Run in five minutes
Requires Python 3.11+; no runtime packages, credentials or network are needed.
```sh
python3 guardian.py
python3 -m unittest discover -v
```

## Design and validation
See ARCHITECTURE.md for boundaries and failure behavior; VALIDATION.md contains actual local test results.
See ADOPTION.md for a reproducible pilot and evidence collection protocol.
Salesforce org integration and security review are pending. Local tests do not validate Apex compilation,
Agentforce behavior, org permissions, limits, or production performance.

## Contributing
Open an issue with a sanitized reproduction, expected behavior and observed result.
Submit changes with a failing regression case and passing test results. Do not submit customer data,
credentials, transcripts, org exports or private metadata. Report security issues privately to the repository owner.

## Attribution
Track human requirements, design decisions, reviews and substantive changes separately from generated code.
Commit identity is not proof of sole authorship. No external-use or impact claim should be made without records.

## Continuous integration
`ci.yml` is the workflow source. The source archive also contains it at `.github/workflows/tests.yml`.
Python CI does not compile Apex or test an activated Agentforce agent.
