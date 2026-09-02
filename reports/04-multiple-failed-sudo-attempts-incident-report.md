# Incident Report — Multiple Failed sudo Attempts

## Incident Summary

Multiple failed `sudo` authentication attempts were detected on the Linux victim host.

The user `saeed` generated three consecutive incorrect sudo password attempts while attempting to execute `/usr/bin/whoami` with elevated privileges.

Splunk successfully ingested the relevant authentication logs, detected the activity using the configured SPL, and triggered the scheduled alert.

Investigation of related authentication events found no evidence of a successful sudo session or successful privilege escalation during the investigated time window.

The activity was confirmed to be part of an authorized SOC lab simulation.

---

## Detection Details

| Field | Value |
|---|---|
| Alert Name | `Multiple Failed sudo Attempts` |
| Detection Source | `/var/log/auth.log` |
| SIEM | Splunk |
| Host | `victim` |
| User | `saeed` |
| Failed Attempts | `3` |
| Requested User | `root` |
| Attempted Command | `/usr/bin/whoami` |
| Alert Type | Scheduled |
| Schedule | Every 5 minutes |
| Detection Threshold | `failed_attempts >= 3` |
| Severity | Medium |

---

## Detection Query

```spl
index=* source="/var/log/auth.log" "incorrect password attempts"
| rex field=_raw "sudo:\s+(?<user>\S+)\s+:\s+(?<failed_attempts>\d+)\s+incorrect password attempts"
| where failed_attempts >= 3
| table _time host user failed_attempts
```

---

## Investigation

The triggered alert was reviewed in Splunk and the returned detection result was validated.

The alert identified:

```text
host = victim
user = saeed
failed_attempts = 3
```

Related sudo authentication activity was then reviewed using:

```spl
index=* source="/var/log/auth.log" host="victim" user="saeed" "sudo"
```

The investigation confirmed repeated sudo authentication failures associated with the user `saeed`.

A separate search was performed to determine whether a successful privileged sudo session followed the failures:

```spl
index=* source="/var/log/auth.log" host="victim" "sudo" "session opened for user root"
```

The search returned:

```text
0 events
```

No successful sudo session was identified during the investigated time window.

---

## Investigation Findings

- Multiple failed `sudo` authentication attempts were observed.
- The affected Linux host was `victim`.
- The associated user was `saeed`.
- Three incorrect password attempts were recorded.
- The requested elevated account was `root`.
- The attempted command was `/usr/bin/whoami`.
- The event was successfully ingested into Splunk.
- The SPL detection successfully identified the activity.
- The configured threshold of three failed attempts was satisfied.
- The scheduled Splunk alert triggered successfully.
- No successful sudo session was identified during the investigated time window.
- No evidence of successful privilege escalation was identified.
- The activity was generated intentionally as part of the authorized Mini SOC lab.

---

## MITRE ATT&CK Mapping

| Field | Mapping |
|---|---|
| Tactic | Privilege Escalation |
| Technique | T1548 — Abuse Elevation Control Mechanism |
| Sub-technique | T1548.003 — Sudo and Sudo Caching |

The activity maps to `T1548.003` because `sudo` is an elevation control mechanism used to execute commands with elevated privileges on Unix and Linux systems.

---

## Analyst Response

The following analyst actions were performed:

- Reviewed the triggered Splunk alert.
- Validated the detection result.
- Reviewed relevant Linux authentication events.
- Confirmed the affected user and host.
- Confirmed the number of incorrect sudo password attempts.
- Identified the attempted elevated command.
- Searched for a successful sudo session following the failed attempts.
- Found no evidence of successful privilege escalation.
- Classified the event as an authorized lab simulation.
- No containment or remediation action was required.

---

## Severity Assessment

**Severity: Medium**

The activity involved repeated attempts to authenticate through `sudo` for elevated command execution.

No successful privilege escalation was identified.

In a production environment, repeated sudo authentication failures could indicate suspicious attempts to obtain elevated privileges and would require investigation of surrounding authentication activity and any subsequent privileged sessions.

---

## Evidence

The following evidence was collected during the investigation:

1. Three failed sudo password attempts generated on the Linux victim host.
2. Raw sudo authentication event ingested into Splunk.
3. SPL detection output showing `host`, `user`, and `failed_attempts`.
4. Validation of the `failed_attempts >= 3` detection threshold.
5. Final Splunk scheduled alert configuration.
6. Successful alert creation confirmation.
7. Triggered alert entry in Splunk.
8. Triggered alert result showing `user=saeed` and `failed_attempts=3`.
9. Investigation of related sudo authentication failures.
10. Search confirming no successful sudo session during the investigated time window.

---

## Final Assessment

The alert was a **true positive for the simulated behavior**.

The detection accurately identified three failed sudo authentication attempts and successfully generated a Splunk alert.

However, the investigation found no evidence that the attempts resulted in a successful privileged session.

### Final Classification

```text
True Positive — Authorized Lab Simulation
```

### Privilege Escalation Outcome

```text
Not Successful
```

---

## Conclusion

This incident validated the complete SOC workflow for detecting repeated failed sudo authentication attempts.

The lab successfully demonstrated:

- Security event generation
- Linux authentication log ingestion
- SPL detection
- Threshold validation
- Scheduled alerting
- Alert triggering
- Investigation
- MITRE ATT&CK mapping
- Incident documentation
- Evidence collection

No successful privilege escalation was identified during the investigation.
