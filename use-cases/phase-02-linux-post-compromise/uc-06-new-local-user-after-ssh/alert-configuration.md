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

```text
600 seconds
