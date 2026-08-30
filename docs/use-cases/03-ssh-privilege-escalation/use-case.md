# SSH Successful Login Followed by Privilege Escalation

## Overview

This use case detects a successful SSH password login followed by the execution of a `sudo` command and the opening of a root session for the same Linux account.

This sequence may indicate that an authenticated remote user successfully elevated privileges after gaining access to the system.

## Objective

The objective is to correlate the following activity:

1. A successful SSH password authentication
2. A `sudo` command executed by the authenticated account
3. A root session opened for the same account
4. All events occurring within a maximum of ten minutes

The detection is designed to distinguish remote privilege escalation from:

- A normal SSH login without privilege escalation
- Local `sudo` activity without a preceding SSH login

## Data Source

The detection relies on Linux authentication events stored in:

```text
/var/log/auth.log
```

Relevant event patterns include:

```text
Accepted password
```

```text
COMMAND=
```

```text
session opened for user root
```

## Lab Configuration

| Setting | Value |
|---|---|
| Splunk index | `main` |
| Monitored host | `victim` |
| Log source | `/var/log/auth.log` |
| SSH source IP | `192.168.56.30` |
| Test account | `soc-test` |
| Privileged account | `root` |
| Authorized test command | `/usr/bin/id` |
| Maximum correlation window | 600 seconds |
| Scheduled search range | Last 15 minutes |
| Alert schedule | Every 5 minutes |
| Alert severity | Critical |
| Alert throttle | 15 minutes |

## Controlled Privilege Configuration

For controlled validation, the `soc-test` account was temporarily permitted to execute only the following command as root:

```text
/usr/bin/id
```

The restricted sudoers rule was configured as:

```text
soc-test ALL=(root) /usr/bin/id
```

This allowed privilege-escalation logging to be tested without granting unrestricted administrative access to the account.

## Detection Query

The validated SPL query is stored in:

```text
detections/ssh-login-followed-by-privilege-escalation.spl
```

The query:

1. Searches for SSH login, sudo command, and root-session events.
2. Classifies each event by activity type.
3. Extracts the SSH username and source IP address.
4. Extracts the account executing the sudo command.
5. Extracts the command executed with elevated privileges.
6. Extracts the account associated with the root session.
7. Sorts the events chronologically.
8. Carries the most recent SSH login context forward.
9. Carries the most recent sudo command context forward.
10. Returns a result only when a root session follows both events.
11. Requires the complete sequence to occur within ten minutes.
12. Produces a separate result for each detected root-session event.

## Detection Sequence

```text
Accepted SSH Password
        ↓
sudo Command Execution
        ↓
Root Session Opened
        ↓
Critical Alert
```

## Detection Output

| Field | Description |
|---|---|
| `host` | Linux system receiving the SSH connection |
| `src_ip` | Source IP address associated with the SSH login |
| `username` | Account associated with the correlated activity |
| `login_time` | Time of the successful SSH authentication |
| `sudo_time` | Time the elevated command was executed |
| `root_session_time` | Time the root session was opened |
| `executed_command` | Command executed using sudo |
| `time_to_sudo_seconds` | Time between SSH login and sudo execution |
| `time_to_root_seconds` | Time between SSH login and root-session creation |

## Positive Validation Test

The positive test was performed using the following authorized sequence:

1. Connected to the victim machine through SSH as `soc-test`.
2. Confirmed the active account using `whoami`.
3. Cleared any existing sudo credential cache.
4. Executed `/usr/bin/id` using sudo.
5. Confirmed that the command executed as `root`.
6. Exited the SSH session.
7. Verified the resulting events in Splunk.

The privileged command returned:

```text
uid=0(root) gid=0(root) groups=0(root)
```

## Validated Detection Results

Two independent privilege-escalation sequences were detected during the final validation.

| Field | First Sequence | Second Sequence |
|---|---:|---:|
| Destination host | `victim` | `victim` |
| Source IP | `192.168.56.30` | `192.168.56.30` |
| Account | `soc-test` | `soc-test` |
| Executed command | `/usr/bin/id` | `/usr/bin/id` |
| Time to sudo | Approximately `11.43` seconds | Approximately `5.68` seconds |
| Time to root | Approximately `11.43` seconds | Approximately `5.68` seconds |
| Detection result | Detected | Detected |

The query returned each privilege-escalation sequence as a separate result.

## Negative Validation Tests

### Test 1: SSH Login Without Privilege Escalation

A successful SSH login was performed using the `soc-test` account.

Only the following activity was executed:

```text
whoami
exit
```

No sudo command was executed and no root session was opened.

The raw SSH login event was present in Splunk, but the correlation query returned:

```text
No results found
```

This confirmed that a normal SSH login does not independently trigger the privilege-escalation detection.

### Test 2: Local Sudo Without SSH Login

The `soc-test` account was accessed locally using `su`, after which the authorized sudo command was executed.

The isolated test window contained local account and sudo activity but did not contain a successful SSH authentication event.

The correlation query returned:

```text
No results found
```

This confirmed that local sudo activity without a preceding SSH login does not independently trigger the detection.

## Validation Matrix

| Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|
| SSH login without sudo | No detection | No detection | Passed |
| Local sudo without SSH login | No detection | No detection | Passed |
| SSH login followed by sudo and root session | Detection | Detection | Passed |
| Multiple independent escalation sequences | Separate results | Separate results | Passed |
| Repeated scheduled searches for the same activity | Duplicate alerts suppressed | Suppressed using throttle | Passed |

## Alert Configuration

| Setting | Value |
|---|---|
| Alert name | `SSH Successful Login Followed by Privilege Escalation` |
| Description | Detects a successful SSH login followed by sudo execution and a root session for the same account |
| Alert type | Scheduled |
| Schedule | Every 5 minutes |
| Cron expression | `*/5 * * * *` |
| Search time range | Last 15 minutes |
| Internal correlation limit | 600 seconds |
| Trigger condition | Number of results is greater than `0` |
| Trigger mode | Once |
| Display mode | Digest |
| Trigger action | Add to Triggered Alerts |
| Severity | Critical |
| Throttle | Enabled |
| Throttle duration | 15 minutes |
| Permissions | Private |

## Why the Search Range Is 15 Minutes

The scheduled search reviews the previous fifteen minutes, while the SPL query requires the correlated activity to occur within ten minutes.

This overlapping search configuration reduces the risk of losing the initial SSH login event at the boundary of a scheduled search window.

The SPL condition remains:

```text
Root session time - SSH login time <= 600 seconds
```

Therefore, the alert may review fifteen minutes of logs but only accepts escalation sequences completed within ten minutes.

## Throttle Validation

Before throttling was enabled, the same activity generated repeated alerts because:

- The alert ran every five minutes
- The search reviewed the previous fifteen minutes
- The same detection remained inside multiple overlapping search windows

A fifteen-minute throttle was enabled to suppress repeated alerts for the same retained detection window.

After throttling was enabled:

1. A new Critical alert was triggered successfully.
2. The next scheduled execution did not create a duplicate alert.
3. The Triggered Alerts page retained one alert for the validated activity.

## Why Critical Severity Was Selected

Critical severity was selected because the detection confirms a complete high-risk sequence:

```text
Remote Authentication
→ Privileged Command Execution
→ Root Session
```

A remote user successfully obtained root-level execution after authenticating through SSH.

In a production environment, this activity could indicate:

- Compromised credentials
- Unauthorized administrative access
- Successful privilege escalation
- Preparation for persistence
- Defense evasion
- Credential access
- Lateral movement
- Sensitive data access

The severity may be reduced when the activity is confirmed as authorized administrative work.

## MITRE ATT&CK Mapping

### Primary Mapping

| Category | Mapping |
|---|---|
| Tactic | Privilege Escalation (`TA0004`) |
| Technique | Abuse Elevation Control Mechanism (`T1548`) |
| Sub-technique | Sudo and Sudo Caching (`T1548.003`) |
| Platform | Linux |

### Related Techniques

| Activity | Mapping |
|---|---|
| Remote SSH access | Remote Services: SSH (`T1021.004`) |
| Use of the local test account | Valid Accounts: Local Accounts (`T1078.003`) |
| Elevated Linux command execution | Sudo and Sudo Caching (`T1548.003`) |

The primary mapping is `T1548.003` because the observed activity uses sudo to execute a command with root privileges.

## Detection Evidence

The following evidence supports the detection:

- Successful SSH password authentication
- Source IP extracted from the SSH event
- Consistent username across the correlated activity
- Sudo command executed by the authenticated account
- `USER=root` recorded in the sudo event
- `/usr/bin/id` recorded as the executed command
- Root session opened for the same account
- Correlation completed within the configured time limit
- Critical alert generated in Splunk
- Duplicate alert suppression confirmed

## Investigation Steps

1. Confirm the source IP address.
2. Confirm the SSH-authenticated username.
3. Review the SSH login timestamp.
4. Identify the command executed using sudo.
5. Confirm that the privileged user was `root`.
6. Review the root-session timestamp.
7. Calculate the time between authentication and escalation.
8. Determine whether the account normally has administrative privileges.
9. Confirm whether the source IP is authorized.
10. Review all commands executed during the SSH session.
11. Search for additional sudo or `su` activity.
12. Review process-creation and network-connection logs.
13. Search for persistence mechanisms.
14. Review access to sensitive files and credentials.
15. Check whether additional hosts were accessed.
16. Preserve relevant authentication and audit logs.
17. Document the classification and response actions.

## Potential False Positives

- Authorized remote administration
- Approved system maintenance
- A legitimate administrator using sudo
- Automated administrative scripts
- Configuration-management activity
- Authorized penetration testing
- Security validation performed inside a lab
- Emergency troubleshooting performed through SSH

## Recommended Response Actions

- Confirm whether the SSH login was authorized.
- Identify the owner and purpose of the source system.
- Terminate unauthorized SSH sessions.
- Temporarily disable or restrict the affected account.
- Reset potentially compromised credentials.
- Revoke exposed SSH keys.
- Review the account's sudo permissions.
- Review `/etc/sudoers` and `/etc/sudoers.d/`.
- Search for additional root-level commands.
- Check for new accounts, services, cron jobs, or SSH keys.
- Review file modifications made after escalation.
- Search for persistence and defense-evasion activity.
- Isolate the host when malicious activity is suspected.
- Preserve logs and forensic evidence.
- Escalate the incident according to the organization's response procedures.

## Limitations

This detection has the following limitations:

- It depends on the Linux authentication-log format used in the lab.
- Index, host, and source values may need adjustment in another environment.
- It detects sudo-based privilege escalation but not all privilege-escalation methods.
- It may not detect kernel exploits, setuid abuse, container escape, or vulnerable services.
- It requires the SSH login, sudo command, and root-session events to be collected.
- Delayed or missing events may prevent successful correlation.
- Concurrent sessions using the same account may reduce source-IP attribution accuracy.
- `/var/log/auth.log` does not provide a single shared identifier across every SSH and sudo event.
- More precise production correlation may require `auditd`, process telemetry, or session identifiers.
- Authorized administrative activity may match the detection.
- The alert throttle is global for the digest alert and may temporarily suppress additional matching activity.

## Recommended Production Improvements

- Collect Linux Audit Framework (`auditd`) events.
- Add process-execution telemetry.
- Correlate terminal, process, and session identifiers.
- Enrich the source IP with reputation and location information.
- Add account privilege and asset criticality context.
- Increase severity for sensitive or privileged accounts.
- Detect unusual commands executed after escalation.
- Monitor changes to sudoers configuration.
- Add command allowlists for approved administrative activity.
- Create separate detections for local and remote privilege escalation.
- Add risk scoring based on source, account, host, and executed command.

## Validation Status

The use case has been:

- Simulated inside an isolated lab
- Verified using raw Linux authentication logs
- Tested using positive and negative scenarios
- Confirmed to reject SSH-only activity
- Confirmed to reject local-sudo-only activity
- Confirmed to detect SSH followed by sudo and root access
- Confirmed to return separate escalation sequences
- Configured as a scheduled Splunk alert
- Triggered successfully with Critical severity
- Tuned using a fifteen-minute throttle
- Documented using validated visual evidence

## Safety Notice

All authentication and privilege-escalation activity used to validate this detection was generated inside an isolated and authorized Mini SOC lab environment.

The account, IP address, host, and privileged command shown in this document belong only to the controlled lab.
