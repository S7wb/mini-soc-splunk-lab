# SSH Successful Login Followed by Privilege Escalation — Incident Report

## Incident Summary

A successful SSH password login followed by sudo execution and root-level command execution was detected on the Linux host `victim`.

The account `soc-test` authenticated remotely from `192.168.56.30`, then executed the authorized command `/usr/bin/id` using sudo. Linux authentication logs confirmed that a sudo session was opened for `root`.

Splunk correlated the sequence and generated a Critical-severity alert.

The activity was intentionally performed inside an isolated and authorized Mini SOC lab.

## Alert Details

| Field | Value |
|---|---|
| Alert Name | `SSH Successful Login Followed by Privilege Escalation` |
| Detection Status | Triggered |
| Classification | True Positive — Authorized Simulation |
| Severity | Critical |
| Incident Status | Closed |
| Alert Time | `2026-07-21 18:05:01 +03:00` |
| Destination Host | `victim` |
| Source IP | `192.168.56.30` |
| Authenticated Account | `soc-test` |
| Privileged Account | `root` |
| Remote Service | SSH |
| Destination Port | `22` |
| Executed Command | `/usr/bin/id` |
| Authentication Method | Password |
| Alert Mode | Digest |
| Throttle | 15 minutes |

## Data Source

| Field | Value |
|---|---|
| Splunk Index | `main` |
| Log Source | `/var/log/auth.log` |
| Monitored Host | `victim` |
| SSH Process | `sshd` |
| Privilege Process | `sudo` |

## Detection Sequence

```text
Successful SSH Password Authentication
                ↓
sudo Command Execution
                ↓
Root Session Opened
                ↓
Critical Splunk Alert
```

## Detection Logic

The detection correlates three Linux authentication events:

1. A successful SSH password authentication
2. A sudo command executed by the authenticated user
3. A sudo session opened for `root`

The sequence must:

- Involve the same Linux account
- Follow the correct chronological order
- Complete within 600 seconds
- Contain the required authentication and privilege events

The validated SPL query is stored in:

```text
detections/ssh-login-followed-by-privilege-escalation.spl
```

## Key Evidence

- `soc-test` successfully authenticated through SSH.
- The source IP was `192.168.56.30`.
- The destination host was `victim`.
- The account executed `/usr/bin/id` using sudo.
- The sudo event recorded `USER=root`.
- A sudo session was opened for `root`.
- The command returned root identity information.
- Splunk correlated the events successfully.
- A Critical-severity alert appeared in Triggered Alerts.
- Throttling prevented repeated alerts from overlapping search windows.

## Command Validation

The privileged command returned:

```text
uid=0(root) gid=0(root) groups=0(root)
```

This confirmed that the command executed with root privileges.

The test account was restricted to the following authorized sudo command:

```text
/usr/bin/id
```

It was not granted unrestricted administrative access.

## Validated Correlation Results

Two independent sequences were returned during final SPL validation.

| Sequence | Source IP | Account | Command | Time to Root |
|---|---|---|---|---:|
| First | `192.168.56.30` | `soc-test` | `/usr/bin/id` | Approximately `11.43` seconds |
| Second | `192.168.56.30` | `soc-test` | `/usr/bin/id` | Approximately `5.68` seconds |

Each root-session event was returned as a separate correlated result.

## Negative Validation Results

### SSH Login Without Privilege Escalation

A successful SSH login was generated without executing sudo.

The raw login event appeared in Splunk, but the privilege-escalation query returned:

```text
No results found
```

### Local Sudo Without SSH Login

The authorized sudo command was executed through a local account session without a preceding SSH login in the isolated test window.

The sudo activity appeared in Splunk, but the correlation query returned:

```text
No results found
```

These tests confirmed that both remote authentication and subsequent privilege activity were required.

## Validation Matrix

| Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|
| SSH login without sudo | No detection | No detection | Passed |
| Local sudo without SSH login | No detection | No detection | Passed |
| SSH login followed by sudo and root session | Detection | Detection | Passed |
| Multiple independent escalation sequences | Separate results | Separate results | Passed |
| Repeated scheduled searches | Duplicate alerts suppressed | Suppressed | Passed |

## Extracted Indicators

| Indicator Type | Value | Description |
|---|---|---|
| Source IP | `192.168.56.30` | Kali Linux simulation system |
| Destination Host | `victim` | Monitored Linux system |
| Account | `soc-test` | Authorized test account |
| Privileged User | `root` | Account used for elevated execution |
| Service | SSH | Initial remote-access service |
| Destination Port | `22` | Default SSH port |
| Executed Command | `/usr/bin/id` | Restricted authorized validation command |

> These indicators belong to the isolated lab environment and are not real-world malicious IOCs.

## Investigation Steps

1. Reviewed the Critical alert in Splunk.
2. Confirmed the source IP and destination host.
3. Identified the SSH-authenticated account.
4. Reviewed the successful authentication timestamp.
5. Identified the sudo command executed by the account.
6. Confirmed that the privileged user was `root`.
7. Reviewed the sudo-session event.
8. Calculated the time from login to elevated execution.
9. Confirmed that the events occurred in chronological order.
10. Verified that the complete sequence occurred within ten minutes.
11. Reviewed whether the account was authorized to use sudo.
12. Confirmed that the test command was restricted to `/usr/bin/id`.
13. Reviewed the Triggered Alerts page.
14. Validated duplicate-alert suppression.
15. Classified and documented the activity.

## Assessment

The observed activity accurately matched the defined detection logic.

In a production environment, remote authentication followed shortly by root-level command execution could indicate:

- Credential compromise
- Unauthorized administrative access
- Successful privilege escalation
- Preparation for persistence
- Defense evasion
- Credential access
- Lateral movement
- Sensitive data access

The incident was classified as a True Positive because Splunk correctly detected the simulated sequence.

No unauthorized compromise occurred because all activity was intentionally generated inside the controlled lab using a restricted test account and command.

## Severity Assessment

Critical severity was assigned because the sequence confirmed:

```text
Remote Login
→ Privileged Command
→ Root-Level Execution
```

Root-level execution provides the highest level of control on a Linux system.

In production, the severity may be reduced only after confirming that:

- The source IP is trusted
- The account owner is authorized
- The command is expected
- The activity matches an approved administrative change
- No suspicious post-escalation behavior occurred

## Recommended Response Actions

In a production environment, the analyst should:

- Confirm whether the SSH login was authorized.
- Contact the account owner or system administrator.
- Terminate unauthorized SSH sessions.
- Temporarily disable or restrict the affected account.
- Reset potentially compromised credentials.
- Revoke exposed SSH keys.
- Review the account's sudo permissions.
- Inspect `/etc/sudoers` and `/etc/sudoers.d/`.
- Review all commands executed after authentication.
- Search for additional root-level activity.
- Check for new accounts and administrative-group changes.
- Review cron jobs, services, and SSH authorized keys.
- Search for persistence and defense-evasion activity.
- Review sensitive file access.
- Check for connections to additional systems.
- Isolate the host if malicious activity is suspected.
- Preserve authentication and forensic evidence.
- Escalate according to the incident-response procedure.

## MITRE ATT&CK Mapping

| Category | Mapping |
|---|---|
| Primary Tactic | Privilege Escalation (`TA0004`) |
| Primary Technique | Abuse Elevation Control Mechanism (`T1548`) |
| Primary Sub-technique | Sudo and Sudo Caching (`T1548.003`) |
| Related Technique | Remote Services: SSH (`T1021.004`) |
| Related Technique | Valid Accounts: Local Accounts (`T1078.003`) |
| Platform | Linux |

## Alert Tuning

The alert runs every five minutes and reviews the previous fifteen minutes.

The SPL query independently requires the login-to-root sequence to complete within 600 seconds.

A fifteen-minute throttle was enabled because the same sequence initially appeared in multiple overlapping search windows.

After throttling:

- A new Critical alert triggered successfully.
- The next scheduled execution did not generate a duplicate.
- One alert remained visible for the retained activity.

## Limitations

- The detection relies on the Linux authentication-log format used in the lab.
- It detects sudo-based elevation but not every privilege-escalation technique.
- Missing SSH, sudo, or session events may prevent correlation.
- Concurrent sessions using the same account may reduce source-IP attribution accuracy.
- `/var/log/auth.log` does not provide one shared identifier across all SSH and sudo events.
- Authorized administration may produce matching activity.
- The digest-alert throttle applies globally and may suppress additional matches temporarily.
- Stronger production correlation may require `auditd`, process telemetry, or session identifiers.

## Closure

The incident was closed as authorized simulated activity after confirming that:

- The activity was generated inside the Mini SOC lab.
- The SSH login was intentionally performed.
- The test account had restricted sudo permission.
- The only authorized privileged command was `/usr/bin/id`.
- Splunk correctly detected and correlated the events.
- The Critical alert triggered successfully.
- Negative validation scenarios did not produce detections.
- Duplicate-alert suppression worked as expected.
- No public, production, or unauthorized system was involved.

## Disclaimer

This incident report documents controlled and authorized activity generated for educational and portfolio purposes only.
