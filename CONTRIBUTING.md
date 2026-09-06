# Contributing

[Use-case roadmap](use-cases/README.md) · [Documentation templates](templates/README.md)

Keep each case in its numbered phase package. Preserve the stable case ID and the lookup name `privileged_accounts.csv`.

Update the roadmap and case documentation together. Treat a case as complete only after source events, ingestion, SPL, alerting, MITRE mapping, investigation, incident reporting, and screenshots have been validated; include automation validation when applicable.

Run the local repository check before submitting structural changes:

```bash
python3 scripts/validate-repository.py
```

This check validates repository structure and local links, not Splunk behavior, technical claims, privacy redaction, or external link availability.
