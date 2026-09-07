# UC-06 — New Local User Created After SSH Login — Alert Configuration

[Use case](README.md)

**Status:** Validated

| Setting | Observed value |
|---|---|
| Search and tested version | Splunk Enterprise — version not recorded during validation |
| Search window / schedule | Last 10 minutes / every 5 minutes (`*/5 * * * *`) |
| Trigger condition / mode | Number of Results `> 0` / Trigger Once |
| Roadmap / configured severity | High / High |
| Throttling fields / period | None configured |
| Alert actions | Add to Triggered Alerts |
| Validation time / timezone | 2026-09-07 10:25:01 / UTC+03:00 |
| Trigger evidence | Captured — filename will be assigned during final evidence organization |

## Alert Name

`New Local User Created After SSH Login`

## Description

Detects the creation of a new local Linux user within 10 minutes after a successful SSH login.

## Detection Window

The correlation logic requires the local account creation event to occur within:

`600 seconds`

after the most recent successful SSH login identified by the detection.

## Validated Result

The scheduled alert successfully triggered during the controlled UC-06 test.

Observed detection result:

| Field | Value |
|---|---|
| Host | `victim` |
| Login user | `soc-test` |
| Login source IP | `192.168.56.30` |
| New local user | `soc-alerttest` |
| Time to account creation | `38.55 seconds` |

## Validation

The following checks were completed successfully:

- Positive detection returned the expected correlated event.
- The scheduled alert executed and appeared in Splunk Triggered Alerts.
- The triggered result identified `soc-test` as the preceding SSH user.
- The triggered result identified `192.168.56.30` as the SSH source IP.
- The created account was identified as `soc-alerttest`.
- Raw `/var/log/auth.log` events confirmed successful account creation.
- A negative test using local account creation was ingested by Splunk but did not satisfy the SSH correlation.
- No successful login or opened session was observed for `soc-alerttest` after account creation.

## Validation Status

**PASS**
