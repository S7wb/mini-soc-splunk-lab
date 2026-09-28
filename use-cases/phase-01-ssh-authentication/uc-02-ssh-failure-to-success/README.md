# SSH Brute Force Followed by Successful Login

**Status:** Validated ✅

[Phase index](../README.md) · [Detection SPL](detection.spl) · [Alert configuration](alert-configuration.md) · [Incident report](incident-report.md) · [Evidence](evidence/README.md)

## Overview

This use case detects repeated failed SSH password authentication attempts followed by a successful login from the same source IP address against the same account.

This authentication pattern may indicate that an attacker successfully guessed, obtained, or reused valid credentials after repeated failed authentication attempts.

The final detection uses sequence-aware correlation to separate independent SSH authentication sequences before evaluating the failure-to-success pattern.

## Objective

The objective is to identify a possible successful SSH account compromise by correlating:

1. Five or more failed SSH password authentication attempts.
2. A subsequent successful SSH password authentication.
3. The same destination host.
4. The same source IP address.
5. The same targeted username.
6. Events belonging to the same authentication sequence.
7. A complete failure-to-success sequence occurring within 600 seconds.

## Data Source

The detection relies on Linux SSH authentication events stored in:

```text
/var/log/auth.log
```

Relevant event types include:

```text
Failed password
```

and:

```text
Accepted password
```

## Lab Configuration

| Setting | Value |
|---|---|
| Splunk index | `main` |
| Monitored host | `victim` |
| Destination IP | `192.168.56.20` |
| Log source | `/var/log/auth.log` |
| Service process | `sshd` |
| Target service | SSH |
| Destination port | `22/TCP` |
| Failure threshold | At least 5 attempts |
| Maximum attack window | 600 seconds |
| Scheduled search range | Last 10 minutes |
| Alert schedule | Every 5 minutes |

## Detection Query

The validated SPL query is stored in:

```text
use-cases/phase-01-ssh-authentication/uc-02-ssh-failure-to-success/detection.spl
```

The final query:

1. Searches for failed and accepted SSH password authentication events.
2. Extracts the authentication result.
3. Extracts the source IP address and username.
4. Handles compressed `message repeated` events when present.
5. Assigns a weight to failed authentication events.
6. Sorts authentication events chronologically.
7. Creates an `auth_sequence` value for sequence-aware correlation.
8. Separates independent authentication sequences.
9. Calculates the failed attempts in each authentication sequence.
10. Identifies the first failed authentication.
11. Identifies the final failed authentication.
12. Identifies the subsequent successful login.
13. Requires at least five failed password authentication attempts.
14. Confirms that the successful login occurred after the failed attempts.
15. Confirms that the complete sequence occurred within 600 seconds.
16. Returns the fields required for SOC investigation.

## Authentication Sequence Correlation

During final validation, the detection correlation logic was improved.

The earlier version aggregated authentication events primarily using:

```text
host + src_ip + username
```

This could combine independent authentication sequences occurring within the same search window.

The final detection creates:

```text
auth_sequence
```

before aggregation.

The final correlation key is:

```text
host + src_ip + username + auth_sequence
```

This allows Splunk to associate each set of failed authentication attempts with the appropriate subsequent successful login.

This sequence-aware correlation reduces the risk of unrelated authentication activity being incorrectly combined into one detection result.

## Detection Output

| Field | Description |
|---|---|
| `host` | Linux system receiving the authentication activity |
| `src_ip` | Source IP address generating the authentication attempts |
| `username` | Account targeted by the activity |
| `failed_attempts` | Failed password authentication attempts associated with the sequence |
| `first_failure` | Time of the first failed authentication |
| `last_failure` | Time of the final failed authentication |
| `successful_login_time` | Time of the subsequent successful authentication |
| `attack_window_seconds` | Time between the first failed attempt and successful authentication |
| `time_after_last_failure_seconds` | Time between the final failed attempt and successful authentication |

## Final Validated Test Result

Final validation was completed inside the isolated Mini SOC lab on `2026-09-28`.

Repeated incorrect SSH passwords were entered against the `soc-test` account from the Kali simulation host.

A successful SSH password authentication then occurred from the same source IP address against the same account.

The final validated result was:

| Field | Validated Result |
|---|---|
| Validation Date | `2026-09-28` |
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
| Detection Result | True Positive — Authorized Simulation |

The result satisfied the detection requirements:

```text
failed_attempts >= 5
```

and:

```text
attack_window_seconds <= 600
```

## Alert Configuration

| Setting | Value |
|---|---|
| Alert Name | `SSH Brute Force Followed by Successful Login` |
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

## Alert Validation

The scheduled alert successfully triggered after the final validation sequence.

| Field | Result |
|---|---|
| Alert Status | Triggered successfully |
| Trigger Time | `2026-09-28 16:40:01 +03` |
| Alert Type | Scheduled |
| Severity | High |
| Mode | Digest |

The triggered alert result matched the manually validated SPL result and displayed the expected investigation fields.

## Search Window Design

The scheduled alert uses:

```text
Last 10 minutes
```

and executes every:

```text
5 minutes
```

The 10-minute scheduler window provides overlap between scheduled executions and reduces the risk of missing a valid authentication sequence near scheduler boundaries.

The detection logic itself still requires:

```text
attack_window_seconds <= 600
```

Therefore, increasing the scheduled search range to 10 minutes does not change the detection threshold.

A valid failure-to-success authentication sequence must still occur within ten minutes.

## Detection Tuning Performed During Validation

Final validation identified a correlation limitation in the earlier SPL implementation.

The previous detection grouped authentication activity using:

```text
host
src_ip
username
```

without explicitly separating independent authentication sequences.

This could cause multiple SSH authentication sequences within the search window to be aggregated together.

The detection was updated to use:

```text
auth_sequence
```

before aggregation.

The final logic correlates using:

```text
host + src_ip + username + auth_sequence
```

The updated SPL was retested successfully and produced the final validated detection and scheduled alert.

The scheduled alert search range was also increased from:

```text
Last 10 minutes
```

to:

```text
Last 10 minutes
```

to provide scheduler overlap while retaining the internal 600-second sequence threshold.

## Evidence

The complete validation evidence is stored in:

```text
evidence/
```

Available evidence:

| # | Evidence |
|---|---|
| 01 | [Raw failure-to-success authentication events](evidence/01-raw-failure-to-success-events.png) |
| 02 | [Validated SPL correlation result](evidence/02-spl-correlation-results.png) |
| 03 | [Final alert configuration](evidence/03-alert-configuration.png) |
| 04 | [Triggered High-severity alert](evidence/04-alert-triggered.png) |
| 05 | [Triggered alert detection result](evidence/05-triggered-alert-results.png) |

Detailed evidence documentation is available in:

[Evidence README](evidence/README.md)

## Detection Lifecycle

The validated detection lifecycle is:

```text
SSH Failed Password Attempts
        ↓
Successful SSH Authentication
        ↓
/var/log/auth.log
        ↓
Splunk Log Ingestion
        ↓
Field Extraction
        ↓
Authentication Sequence Separation
        ↓
Sequence-Aware SPL Correlation
        ↓
Detection Result
        ↓
Scheduled Alert
        ↓
High-Severity Triggered Alert
        ↓
SOC Investigation
        ↓
Incident Documentation
```

## Why High Severity Was Selected

High severity was selected because the detection confirms that a successful SSH password authentication occurred after repeated failed password attempts.

This pattern provides stronger evidence of possible credential compromise than failed authentication attempts alone.

Additional evidence may warrant further escalation, including:

- Successful authentication to the `root` account
- Authentication to an administrative or privileged account
- Privilege escalation after login
- Suspicious command execution
- Persistence activity
- Sensitive file or data access
- Lateral movement
- Connections to additional systems
- Activity from a known malicious source

## Investigation Steps

1. Review the triggered Splunk alert.
2. Confirm the destination host.
3. Confirm the destination IP address.
4. Confirm the source IP address.
5. Identify the targeted username.
6. Review the number of failed password authentication attempts.
7. Review the first and final failed-authentication timestamps.
8. Confirm that a successful authentication followed the failed attempts.
9. Verify that the source IP address and username match across the correlated sequence.
10. Verify that the events belong to the same authentication sequence.
11. Calculate the full failure-to-success attack window.
12. Calculate the delay between the final failure and successful authentication.
13. Confirm that the sequence occurred within the configured 600-second threshold.
14. Review the authenticated SSH session.
15. Search for commands executed after authentication.
16. Search for `sudo`, `su`, or other privilege-escalation activity.
17. Review processes created by the authenticated account.
18. Review network connections associated with the session.
19. Search for additional authentication attempts from the same source.
20. Determine whether the login was authorized.
21. Preserve relevant logs and forensic evidence.
22. Document the final classification and response actions.

## Potential False Positives

Potential legitimate scenarios include:

- A legitimate user repeatedly entering an incorrect password before remembering it
- An administrator using outdated credentials
- A password-management or automation issue
- An authorized penetration test
- A security validation exercise
- A user changing a password while temporarily continuing to use the previous credential

Additional account, asset, source, and behavioral context should be reviewed before determining whether the authentication activity is malicious.

## Recommended Response Actions

In a production environment:

- Confirm whether the successful login was authorized
- Review the affected account's authentication history
- Temporarily lock or protect the account when compromise is suspected
- Terminate suspicious SSH sessions
- Reset the account password when appropriate
- Revoke exposed credentials or SSH keys
- Block or restrict the source IP address when confirmed unauthorized
- Review commands executed after authentication
- Search for privilege escalation
- Search for persistence
- Review processes started by the authenticated user
- Review network connections associated with the session
- Search other systems for related authentication activity
- Review whether additional accounts were targeted
- Preserve relevant authentication logs and forensic evidence
- Escalate the incident if privileged access, persistence, lateral movement, or sensitive-data access is identified

## MITRE ATT&CK Mapping

| Category | Mapping |
|---|---|
| Tactic | Credential Access (`TA0006`) |
| Technique | Brute Force (`T1110`) |
| Sub-technique | Password Guessing (`T1110.001`) |
| Platform | Linux |
| Targeted Service | SSH (`22/TCP`) |

## Limitations

This detection may not independently identify:

- Successful authentication using SSH keys
- Distributed password attacks from multiple source IP addresses
- Low-and-slow attacks that remain below the configured threshold
- Password attempts distributed across multiple usernames
- Authentication events stored in another index or log source
- Authentication activity that does not produce the expected Linux SSH log format
- Post-authentication activity performed outside this detection's scope
- Credential compromise without preceding failed password attempts

Separate detections and hunting logic should be used for these scenarios.

## Validation Status

**UC-02 Status: Validated ✅**

The following components were successfully verified:

- SSH authentication log ingestion
- Failed password event detection
- Successful authentication event detection
- Source IP extraction
- Username extraction
- Authentication sequence separation
- Failure threshold evaluation
- 600-second correlation threshold
- Sequence-aware SPL correlation
- Expected detection output
- Scheduled alert execution
- High-severity alert generation
- Triggered Alerts verification
- Triggered alert result verification
- Incident investigation
- Evidence collection
- Detection tuning documentation
- Incident report documentation

## Safety Notice

All authentication activity used to validate this detection was generated inside an isolated and authorized Mini SOC lab environment.

The IP addresses, systems, and user accounts documented in this use case belong only to the controlled lab.

No unauthorized external systems or production environments were targeted.
