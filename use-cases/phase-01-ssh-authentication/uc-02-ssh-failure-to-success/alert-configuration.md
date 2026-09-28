# SSH Brute Force Followed by Successful Login — Alert Configuration

[Use case](README.md) · [Detection SPL](detection.spl) · [Evidence](evidence/README.md)

## Overview

This document describes the Splunk alert configuration used to detect repeated failed SSH password authentication attempts followed by a successful login from the same source IP address and against the same account.

This authentication sequence may indicate that an attacker successfully guessed, obtained, or reused valid credentials.

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
use-cases/phase-01-ssh-authentication/uc-02-ssh-failure-to-success/detection.spl
```

The query:

1. Searches for failed and accepted SSH password authentication events.
2. Extracts the authentication result.
3. Extracts the source IP address and username.
4. Handles compressed `message repeated` events when present.
5. Assigns a weight to failed authentication events.
6. Sorts events chronologically for each host, source IP, and username.
7. Uses `auth_sequence` to separate individual authentication sequences.
8. Calculates the failed attempts belonging to each authentication sequence.
9. Identifies the first and last failed authentication events.
10. Identifies the subsequent successful login.
11. Requires at least five failed attempts.
12. Confirms that the successful login occurred after the failures.
13. Confirms that the complete failure-to-success sequence occurred within 600 seconds.
14. Returns the relevant fields required for SOC investigation.

## Authentication Sequence Correlation

The detection uses:

```text
auth_sequence
```

to prevent unrelated authentication activity from being combined into the same detection result.

Authentication events are grouped by:

- Destination host
- Source IP address
- Username
- Authentication sequence

This ensures that failed attempts are correlated with the appropriate subsequent successful login instead of being combined with unrelated historical login activity.

## Alert Workflow

1. Failed SSH password attempts are recorded in `/var/log/auth.log`.
2. Splunk Universal Forwarder sends the authentication events to Splunk Enterprise.
3. A successful SSH password login occurs after repeated failures.
4. The scheduled alert runs every five minutes.
5. The scheduled search reviews the previous 10 minutes of authentication activity.
6. The SPL query separates authentication sequences using `auth_sequence`.
7. The query correlates events by destination host, source IP address, username, and authentication sequence.
8. A result is returned when five or more failed attempts are followed by a successful login within 600 seconds.
9. Splunk adds the alert to the Triggered Alerts page with High severity.
10. The analyst reviews the correlated result and begins investigation.

## Detection Output

| Field | Description |
|---|---|
| `host` | Linux system receiving the authentication activity |
| `src_ip` | Source IP address generating the attempts |
| `username` | Account targeted by the activity |
| `failed_attempts` | Number of failed password authentication attempts in the sequence |
| `first_failure` | Time of the first failed attempt |
| `last_failure` | Time of the final failed attempt |
| `successful_login_time` | Time of the subsequent successful authentication |
| `attack_window_seconds` | Time between the first failure and successful login |
| `time_after_last_failure_seconds` | Time between the final failure and successful login |

## Validated Alert Test

The alert was validated using controlled SSH authentication activity inside the isolated Mini SOC lab on `2026-09-28`.

Repeated incorrect SSH passwords were entered against the test account, followed by a successful login from the same source IP address.

The validated detection produced the following result:

| Field | Validated Result |
|---|---|
| Alert Status | Triggered successfully |
| Alert Trigger Time | `2026-09-28 16:40:01 +03` |
| Destination Host | `victim` |
| Destination IP | `192.168.56.20` |
| Source IP | `192.168.56.30` |
| Targeted Account | `soc-test` |
| Failed Attempts | `6` |
| First Failure | `2026-09-28 16:32:53.670766` |
| Last Failure | `2026-09-28 16:32:57.331134` |
| Successful Login | `2026-09-28 16:33:01.543799` |
| Attack Window | `7.87 seconds` |
| Time After Final Failure | `4.21 seconds` |
| Severity | High |
| Alert Type | Scheduled |

The alert appeared successfully in the Splunk Triggered Alerts page during the next scheduled execution.

The triggered alert result displayed the expected investigation fields and matched the manually validated SPL result.

## Detection Tuning Performed During Validation

During final validation, the original correlation logic was reviewed and improved.

The previous version grouped events using only:

```text
host + src_ip + username
```

This could cause unrelated authentication sequences occurring within the search window to be combined into one result.

The detection was updated to create an `auth_sequence` value before aggregation.

The final correlation key is:

```text
host + src_ip + username + auth_sequence
```

This separates individual failure-to-success authentication sequences and reduces the risk of incorrect event correlation.

The updated detection was retested successfully before final validation.

## Why High Severity Was Selected

High severity was selected because the alert confirms that a successful SSH password authentication occurred after repeated failed attempts.

This sequence provides stronger evidence of possible credential compromise than failed login attempts alone.

The severity may require escalation when additional evidence is observed, including:

- Successful authentication to the `root` account
- Authentication to an administrative account
- Privilege escalation after login
- Suspicious command execution
- Persistence activity
- Sensitive data access
- Connections to additional systems
- Activity from a known malicious source

## Search Window Requirement

The scheduled alert uses the following rolling search window:

```text
Last 10 minutes
```

The alert executes every five minutes.

The 10-minute scheduler window provides sufficient overlap for Splunk to observe the complete authentication sequence even when the activity occurs near the boundary between scheduled executions.

The detection logic itself still requires:

```text
attack_window_seconds <= 600
```

Therefore, increasing the scheduled search window to 10 minutes does not change the detection requirement.

A valid failure-to-success sequence must still occur within 600 seconds.

The scheduled alert is not intended to run over `All time`.

Historical threat hunting should use an appropriately bounded time range and investigation-specific search logic.

## Recommended Production Tuning

| Setting | Tuning Consideration |
|---|---|
| Failure threshold | Adjust based on normal authentication behavior |
| Detection sequence | Maintain sequence-aware correlation to avoid unrelated event grouping |
| Search window | Adjust for scheduling overlap or low-and-slow attack scenarios |
| Schedule | Align with the configured search window and ingestion latency |
| Severity | Increase when privileged accounts or post-login activity are involved |
| Throttling | Enable when duplicate alerts create excessive noise |
| Allowlisting | Exclude approved scanners or administration systems only when justified |
| Account context | Increase priority for privileged or sensitive accounts |
| Source enrichment | Add GeoIP, reputation, asset, or identity context |
| Ingestion delay | Account for delayed events when tuning the scheduled search window |

## Validation Status

The alert configuration has been:

- Configured in Splunk Enterprise
- Updated with sequence-aware authentication correlation
- Tested using controlled authentication activity
- Validated with six failed password attempts followed by a successful login
- Triggered successfully as a scheduled alert
- Verified in the Triggered Alerts page
- Confirmed to display the expected investigation fields
- Assigned High severity
- Documented using validated lab evidence

## Safety Notice

All authentication activity used to validate this alert was generated inside an isolated and authorized Mini SOC lab environment.

The account, source IP address, and destination system shown in this document belong only to the controlled lab.
