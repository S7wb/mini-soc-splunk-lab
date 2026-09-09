# UC-06 — New Local User Created After SSH Login

[Phase index](../README.md) · [Detection SPL](detection.spl) · [Alert configuration](alert-configuration.md) · [Incident report](incident-report.md) · [Evidence](evidence/README.md)

**Status:** Validated

**Roadmap severity:** High

## Objective

Detect the creation of a new local Linux user shortly after a successful SSH login.

This behavior can indicate persistence activity after an attacker obtains remote access to a Linux system.

## Scenario

The use case was executed in the authorized Mini SOC lab using the following sequence:

```text
Kali / SSH Source
192.168.56.30
        |
        | Successful SSH login
        v
Victim Linux
192.168.56.20
        |
        | soc-test
        | sudo /usr/sbin/useradd soc-alerttest
        v
New Local Account
soc-alerttest
        |
        v
/var/log/auth.log
        |
        v
Splunk Detection
        |
        v
Scheduled High-Severity Alert
```

## Data Source

| Field | Value |
|---|---|
| Host | `victim` |
| Victim IP | `192.168.56.20` |
| SSH source IP | `192.168.56.30` |
| Log source | `/var/log/auth.log` |
| Sourcetype | `linux_secure` |
| SSH account | `soc-test` |
| Test account created | `soc-alerttest` |

Splunk ingestion was verified before detection validation.

## Detection Logic

The detection correlates two events on the Linux victim host:

1. A successful SSH authentication event containing `Accepted password for`.
2. A successful local account creation event containing `new user:`.

The account creation must occur within `600 seconds` of the preceding successful SSH login.

The tested SPL is stored in:

[`detection.spl`](detection.spl)

### Detection Output

The detection returns:

- Host
- Preceding SSH user
- SSH source IP
- Newly created local account
- Time between SSH login and account creation

## Positive Test

The final controlled validation used:

- SSH user: `soc-test`
- SSH source: `192.168.56.30`
- Created account: `soc-alerttest`

The detection successfully correlated the account creation with the preceding SSH login.

Observed result:

| Field | Value |
|---|---|
| Host | `victim` |
| Login user | `soc-test` |
| Login source IP | `192.168.56.30` |
| New user | `soc-alerttest` |
| Time to creation | `38.55 seconds` |

**Positive test:** PASS

## Negative Test

A separate account, `soc-localtest`, was created locally on the victim system without a qualifying SSH login in the correlation search window.

The `new user:` event was successfully ingested into Splunk, confirming that the account creation itself was visible to the detection pipeline.

The UC-06 correlation returned:

```text
0 events
```

This demonstrated that the detection did not trigger solely because a local account was created.

**Negative test:** PASS

## Alert Validation

A scheduled Splunk alert was configured as:

| Setting | Value |
|---|---|
| Alert name | `New Local User Created After SSH Login` |
| Severity | High |
| Search range | Last 10 minutes |
| Schedule | Every 5 minutes |
| Cron | `*/5 * * * *` |
| Trigger condition | Number of Results `> 0` |
| Trigger mode | Trigger Once |
| Action | Add to Triggered Alerts |

The scheduled alert successfully triggered at:

`2026-09-07 10:25:01 UTC+03:00`

The triggered result identified:

```text
login_user      = soc-test
login_src_ip    = 192.168.56.30
new_user        = soc-alerttest
time_to_creation = 38.55 seconds
```

**Alert validation:** PASS

Full configuration:

[Alert configuration](alert-configuration.md)

## Investigation Summary

The investigation confirmed that:

- `soc-test` successfully authenticated to the victim through SSH.
- The SSH connection originated from `192.168.56.30`.
- `soc-test` subsequently executed `/usr/sbin/useradd soc-alerttest` using `sudo`.
- `/var/log/auth.log` recorded successful creation of the new local account.
- Splunk correlated the account creation with the preceding SSH login.
- The scheduled High-severity alert triggered successfully.
- No successful login or opened session using `soc-alerttest` was observed after account creation during the investigation window.

Full investigation:

[Incident report](incident-report.md)

## MITRE ATT&CK Mapping

| Tactic | Technique | Sub-technique |
|---|---|---|
| Persistence (`TA0003`) | Create Account (`T1136`) | Local Account (`T1136.001`) |

The behavior represents creation of a local account that could be used to maintain access to a Linux system.

## Detection Limitations

The current implementation is intentionally scoped to the lab environment.

Key limitations:

- Correlation is performed using the most recent successful SSH login observed on the host within the configured correlation window.
- The detection does not prove that the correlated SSH user directly caused every subsequent account creation.
- Multiple simultaneous SSH sessions on the same host could create attribution ambiguity.
- Stronger production correlation could use session, process, audit, or endpoint telemetry.
- Detection depends on the observed Linux authentication-log format and successful `useradd` logging.

These limitations are documented to avoid overstating the detection's attribution capability.

## Completion Checklist

- [x] Generate the scenario in the authorized lab.
- [x] Verify source events and ingestion into Splunk.
- [x] Develop the SPL detection.
- [x] Validate a positive scenario.
- [x] Validate a negative scenario.
- [x] Configure the scheduled alert.
- [x] Confirm the alert appears in Triggered Alerts.
- [x] Investigate the detected activity.
- [x] Map the behavior to MITRE ATT&CK.
- [x] Complete the incident report.
- [x] Finalize evidence filenames and captions.
- [ ] Complete final repository QA.

## Validation Result

**PASS**

UC-06 detection and alert behavior were successfully implemented and validated in the authorized Mini SOC lab.

The use case will be marked fully complete after the final evidence organization and repository QA are completed.
