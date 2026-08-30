# SSH Brute Force Followed by Successful Login — Alert Configuration

## Overview

This document describes the Splunk alert configuration used to detect repeated failed SSH password attempts followed by a successful login from the same source IP address and against the same account.

This authentication sequence may indicate that an attacker successfully guessed or obtained valid credentials.

## Alert Details

| Setting | Value |
|---|---|
| Alert Name | `SSH Brute Force Followed by Successful Login` |
| Description | Detects repeated failed SSH login attempts followed by a successful login from the same source IP and account |
| Alert Type | Scheduled |
| Schedule | Every 5 minutes |
| Cron Expression | `*/5 * * * *` |
| Search Time Range | Last 10 minutes |
| Trigger Condition | Number of results is greater than `0` |
| Trigger Mode | Once |
| Trigger Action | Add to Triggered Alerts |
| Severity | High |
| Throttle | Disabled |
| Display Mode | Digest |
| Permissions | Private |

## Detection Query

The alert uses the validated SPL query stored in:

```text
detections/ssh-bruteforce-followed-by-success.spl
```

The query:

1. Searches for failed and accepted SSH password events.
2. Extracts the authentication result.
3. Extracts the source IP address and username.
4. Handles compressed `message repeated` events.
5. Calculates the total number of failed attempts.
6. Identifies the first and last failed authentication events.
7. Identifies the successful login event.
8. Confirms that the success occurred after the failed attempts.
9. Confirms that the full sequence occurred within ten minutes.
10. Returns the relevant fields for investigation.

## Alert Workflow

1. Failed SSH password attempts are recorded in `/var/log/auth.log`.
2. Splunk Universal Forwarder sends the authentication events to Splunk Enterprise.
3. A successful SSH password login occurs after the failures.
4. The scheduled alert runs every five minutes.
5. The search reviews the previous ten minutes.
6. The SPL query correlates events by destination host, source IP, and username.
7. A result is returned when five or more failures are followed by a successful login.
8. Splunk adds the alert to the Triggered Alerts page with High severity.
9. The analyst reviews the result and begins investigation.

## Detection Output

| Field | Description |
|---|---|
| `host` | Linux system receiving the authentication activity |
| `src_ip` | Source IP address generating the attempts |
| `username` | Account targeted by the activity |
| `failed_attempts` | Total failed password attempts |
| `first_failure` | Time of the first failed attempt |
| `last_failure` | Time of the final failed attempt |
| `successful_login_time` | Time of the successful authentication |
| `attack_window_seconds` | Time between the first failure and successful login |
| `time_after_last_failure_seconds` | Time between the final failure and successful login |

## Validated Alert Test

The alert was tested using controlled SSH authentication activity inside the Mini SOC lab.

Five incorrect passwords were entered against the test account, followed by a successful login from the same source IP address.

| Field | Validated Result |
|---|---|
| Alert Status | Triggered successfully |
| Alert Time | `2026-07-19 21:55:01 +03:00` |
| Destination Host | `victim` |
| Source IP | `192.168.56.30` |
| Targeted Account | `soc-test` |
| Failed Attempts | `5` |
| First Failure | `2026-07-19 21:51:33 +03:00` |
| Last Failure | `2026-07-19 21:51:39 +03:00` |
| Successful Login | `2026-07-19 21:51:46 +03:00` |
| Attack Window | Approximately `12.69` seconds |
| Time After Final Failure | Approximately `6.49` seconds |
| Severity | High |

The alert appeared successfully in the Splunk Triggered Alerts page after the next scheduled execution.

## Why High Severity Was Selected

High severity was selected because the alert confirms that a successful SSH password authentication occurred after repeated failed attempts.

This sequence provides stronger evidence of possible credential compromise than failed login attempts alone.

The severity should be increased to Critical when additional evidence is observed, including:

- Successful authentication to the `root` account
- Authentication to an administrative account
- Privilege escalation after login
- Suspicious command execution
- Persistence activity
- Sensitive data access
- Connections to additional systems
- Activity from a known malicious source

## Search Window Requirement

The alert is designed to operate using a limited rolling search window:

```text
Last 10 minutes
```

The query should not normally be executed over `All time` because unrelated historical authentication attempts may be grouped together when they share the same host, source IP, and username.

A separate historical-hunting query would require sessionization or time-based grouping to isolate individual failure-to-success sequences.

## Recommended Production Tuning

| Setting | Tuning Consideration |
|---|---|
| Failure threshold | Adjust based on normal authentication behavior |
| Search window | Increase for low-and-slow attacks when required |
| Schedule | Align with the configured search window |
| Severity | Increase when privileged accounts or post-login activity are involved |
| Throttling | Enable when duplicate alerts create excessive noise |
| Allowlisting | Exclude approved scanners or administration systems when justified |
| Account context | Increase priority for privileged or sensitive accounts |
| Source enrichment | Add GeoIP, reputation, or asset-context information |

## Validation Status

The alert configuration has been:

- Configured in Splunk Enterprise
- Tested using controlled authentication activity
- Triggered successfully
- Verified in the Triggered Alerts page
- Confirmed to display the expected investigation fields
- Assigned High severity
- Documented using validated lab evidence

## Safety Notice

All authentication activity used to validate this alert was generated inside an isolated and authorized Mini SOC lab environment.

The account, source IP address, and destination system shown in this document belong only to the controlled lab.
