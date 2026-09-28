# SSH Brute Force Followed by Successful Login — Incident Report

[Use case](README.md) · [Detection SPL](detection.spl) · [Evidence](evidence/README.md)

## Incident Summary

A sequence of repeated failed SSH password authentication attempts followed by a successful login was detected against the Linux host `victim` in the Mini SOC lab.

Six failed password authentication attempts targeting the account `soc-test` originated from `192.168.56.30`. A successful SSH password login from the same source IP address and against the same account occurred `4.21 seconds` after the final failed attempt.

The complete failure-to-success authentication sequence occurred within `7.87 seconds`.

Splunk successfully correlated the authentication events using the updated sequence-aware detection logic and generated a scheduled High-severity alert.

The activity was intentionally generated inside an isolated and authorized lab environment.

## Alert Details

| Field | Value |
|---|---|
| Alert Name | `SSH Brute Force Followed by Successful Login` |
| Detection Status | Triggered |
| Classification | True Positive — Authorized Simulation |
| Severity | High |
| Incident Status | Closed |
| Alert Type | Scheduled |
| Alert Trigger Time | `2026-09-28 16:40:01 +03` |
| Destination Host | `victim` |
| Destination IP | `192.168.56.20` |
| Source IP | `192.168.56.30` |
| Targeted Account | `soc-test` |
| Targeted Service | SSH |
| Destination Port | `22` |
| Failed Attempts | `6` |
| First Failure | `2026-09-28 16:32:53.670766` |
| Last Failure | `2026-09-28 16:32:57.331134` |
| Successful Login | `2026-09-28 16:33:01.543799` |
| Attack Window | `7.87 seconds` |
| Time After Final Failure | `4.21 seconds` |

## Data Source

| Field | Value |
|---|---|
| Splunk Index | `main` |
| Log Source | `/var/log/auth.log` |
| Service Process | `sshd` |
| Monitored Host | `victim` |
| Destination IP | `192.168.56.20` |

## Detection Logic

The detection correlates Linux SSH authentication events containing:

```text
Failed password
```

and:

```text
Accepted password
```

The detection triggers when:

1. Five or more failed SSH password authentication attempts are observed.
2. The failed attempts target the same username.
3. The failed attempts originate from the same source IP address.
4. The authentication activity targets the same destination host.
5. A successful password authentication occurs after the failed attempts.
6. The failed and successful events belong to the same authentication sequence.
7. The complete failure-to-success sequence occurs within `600 seconds`.

The validated SPL query is stored in:

```text
use-cases/phase-01-ssh-authentication/uc-02-ssh-failure-to-success/detection.spl
```

## Authentication Sequence Correlation

During final validation, the detection logic was improved to prevent unrelated authentication events from being combined into the same detection result.

The original correlation logic grouped authentication events using:

```text
host + src_ip + username
```

This could combine multiple independent authentication sequences occurring within the same scheduled search window.

The updated detection creates an `auth_sequence` value before aggregation.

The final correlation key is:

```text
host + src_ip + username + auth_sequence
```

This allows Splunk to associate failed authentication attempts with the appropriate subsequent successful login.

The updated sequence-aware detection was successfully retested before final validation.

## Scheduled Alert Configuration

The validated scheduled alert uses:

| Setting | Value |
|---|---|
| Search Time Range | Last 10 minutes |
| Schedule | Every 5 minutes |
| Cron Expression | `*/5 * * * *` |
| Trigger Condition | Number of results is greater than `0` |
| Trigger Mode | Once |
| Trigger Action | Add to Triggered Alerts |
| Severity | High |
| Throttle | Disabled |

The 10-minute scheduled search window provides overlap between alert executions and helps prevent a valid failure-to-success sequence from being missed near scheduler boundaries.

The detection requirement itself remains:

```text
attack_window_seconds <= 600
```

Therefore, the increased scheduler window does not change the detection threshold. A valid failure-to-success authentication sequence must still occur within ten minutes.

## Key Evidence

- Six failed SSH password authentication attempts targeted `soc-test`.
- All correlated attempts originated from `192.168.56.30`.
- The destination system was `victim` at `192.168.56.20`.
- A successful SSH password authentication followed the failed attempts.
- The successful authentication occurred `4.21 seconds` after the final failed attempt.
- The complete failure-to-success sequence occurred within `7.87 seconds`.
- The detection returned the expected correlation fields.
- The scheduled Splunk alert triggered successfully.
- The alert appeared in the Splunk Triggered Alerts page.
- The triggered alert was assigned High severity.
- The triggered alert result matched the manually validated SPL result.

## Extracted Indicators

| Indicator Type | Value | Description |
|---|---|---|
| Source IP | `192.168.56.30` | Kali Linux simulation host |
| Destination IP | `192.168.56.20` | Monitored Ubuntu Linux system |
| Destination Host | `victim` | Monitored Linux system |
| Targeted Account | `soc-test` | Test account involved in the simulation |
| Service | SSH | Targeted remote-access service |
| Destination Port | `22` | Default SSH service port |
| Authentication Pattern | Failed attempts followed by successful login | Potential credential-compromise pattern |

> The displayed IP addresses are internal lab addresses used for authorized testing and are not real-world malicious indicators.

## Investigation Steps

1. Reviewed the High-severity Splunk triggered alert.
2. Confirmed the destination host and destination IP address.
3. Confirmed the source IP address.
4. Identified the targeted account.
5. Reviewed the number of failed password authentication attempts.
6. Reviewed the timestamp of the first failed authentication.
7. Reviewed the timestamp of the final failed authentication.
8. Confirmed that a successful authentication followed the failures.
9. Verified that the source IP address and username matched across the correlated sequence.
10. Verified that the events belonged to the same authentication sequence.
11. Calculated the complete failure-to-success attack window.
12. Calculated the delay between the final failed authentication and successful login.
13. Confirmed that the sequence remained within the configured `600-second` detection threshold.
14. Reviewed the scheduled alert execution.
15. Confirmed that Splunk generated the alert successfully.
16. Verified the detection result through the Triggered Alerts page.
17. Determined whether the activity was authorized.
18. Documented the evidence and recommended production response actions.

## Timeline

| Time | Event |
|---|---|
| `2026-09-28 16:32:53.670766` | First failed SSH password authentication in the correlated sequence |
| `2026-09-28 16:32:57.331134` | Final failed SSH password authentication |
| `2026-09-28 16:33:01.543799` | Successful SSH password authentication |
| `2026-09-28 16:40:01 +03` | Scheduled Splunk alert triggered |

The time between the first failed authentication and successful login was:

```text
7.87 seconds
```

The time between the final failed authentication and successful login was:

```text
4.21 seconds
```

## Assessment

The activity matched the defined detection conditions for repeated SSH password authentication failures followed by successful authentication.

The detection identified:

```text
6 failed password attempts
        ↓
successful SSH authentication
        ↓
same host
same source IP
same username
same authentication sequence
        ↓
7.87-second total attack window
```

In a production environment, this pattern may indicate that credentials were successfully guessed, obtained, or reused after repeated failed authentication attempts.

The incident was classified as a True Positive because the detection accurately identified the intentionally generated failure-to-success authentication sequence.

No unauthorized compromise occurred because the activity was generated inside the controlled and isolated Mini SOC lab.

## Detection Engineering Findings

Final validation identified a correlation limitation in the earlier version of the SPL query.

The previous query aggregated events primarily by:

```text
host
src_ip
username
```

This design could correlate authentication events from separate login sequences when they occurred within the same search window.

The detection was therefore updated to use sequence-aware correlation through:

```text
auth_sequence
```

The final SPL separates authentication sequences before calculating the failed-attempt count and successful-login relationship.

This tuning improves detection accuracy and reduces the risk of unrelated authentication events being incorrectly grouped together.

The scheduled search window was also increased from:

```text
Last 10 minutes
```

to:

```text
Last 10 minutes
```

while maintaining the detection requirement:

```text
attack_window_seconds <= 600
```

This provides scheduler overlap without changing the intended ten-minute attack-sequence threshold.

## Recommended Response Actions

In a production environment, the analyst should:

- Confirm whether the successful SSH login was authorized.
- Review the affected account's authentication history.
- Temporarily lock or protect the affected account when compromise is suspected.
- Terminate suspicious SSH sessions.
- Reset the affected account password when appropriate.
- Revoke exposed credentials or SSH keys.
- Block or restrict the source IP address when confirmed unauthorized.
- Review commands executed after successful authentication.
- Search for `sudo`, `su`, and privilege-escalation activity.
- Investigate persistence mechanisms created after authentication.
- Review processes started by the authenticated user.
- Review outbound and lateral network connections associated with the session.
- Search other systems for authentication attempts from the same source.
- Review whether other accounts were targeted.
- Preserve relevant authentication logs and forensic evidence.
- Escalate the incident if privileged access, persistence, lateral movement, or sensitive-data access is identified.

## MITRE ATT&CK Mapping

| Category | Mapping |
|---|---|
| Tactic | Credential Access (`TA0006`) |
| Technique | Brute Force (`T1110`) |
| Sub-technique | Password Guessing (`T1110.001`) |
| Platform | Linux |
| Targeted Service | SSH (`22/TCP`) |

## Closure

The incident was closed as authorized simulated activity after confirming that:

- The authentication attempts were intentionally generated inside the Mini SOC lab.
- Six failed SSH password authentication attempts were successfully correlated with the subsequent successful login.
- The detection used sequence-aware correlation through `auth_sequence`.
- The complete detected sequence occurred within `7.87 seconds`.
- The scheduled Splunk alert triggered successfully.
- The alert appeared in the Triggered Alerts page with High severity.
- The triggered alert result contained the expected investigation fields.
- The activity involved only dedicated lab systems and accounts.
- No unauthorized production system or external target was involved.

## Validation Status

UC-02 incident validation has been completed successfully.

The following components were verified:

- SSH authentication logs ingested successfully
- Failed authentication events detected
- Successful authentication event detected
- Source IP extracted correctly
- Username extracted correctly
- Authentication sequences separated correctly
- Failure threshold enforced
- Ten-minute sequence threshold enforced
- SPL detection returned the expected result
- Scheduled alert executed successfully
- High-severity alert triggered successfully
- Triggered alert result verified
- Evidence captured
- Detection tuning documented

## Disclaimer

This incident report documents controlled and authorized activity generated inside an isolated lab environment for cybersecurity education, detection engineering practice, SOC analysis training, and portfolio purposes only.
