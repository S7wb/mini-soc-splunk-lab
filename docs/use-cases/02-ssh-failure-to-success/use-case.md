# SSH Brute Force Followed by Successful Login

## Overview

This use case detects repeated failed SSH login attempts followed by a successful login from the same source IP address against the same account.

This sequence may indicate that an attacker successfully guessed or obtained valid credentials.

## Objective

The objective is to identify a possible successful SSH account compromise by correlating:

1. Five or more failed password attempts
2. A subsequent successful password authentication
3. The same source IP address
4. The same targeted username
5. Activity occurring within ten minutes

## Data Source

The detection relies on Linux SSH authentication events stored in:

```text
/var/log/auth.log
```

Relevant event types include:

```text
Failed password
```

```text
Accepted password
```

## Lab Configuration

| Setting | Value |
|---|---|
| Splunk index | `main` |
| Monitored host | `victim` |
| Log source | `/var/log/auth.log` |
| Service process | `sshd` |
| Failure threshold | 5 attempts |
| Maximum attack window | 600 seconds |
| Recommended search range | Last 10 minutes |

## Detection Query

The validated SPL query is stored in:

```text
detections/ssh-bruteforce-followed-by-success.spl
```

The query:

1. Searches for failed and accepted SSH password events.
2. Extracts the authentication result.
3. Extracts the source IP address and username.
4. Handles compressed `message repeated` events.
5. Calculates the total failed attempts.
6. Identifies the first and last failed attempts.
7. Identifies the successful login time.
8. Confirms that the successful login occurred after the failures.
9. Confirms that the sequence occurred within ten minutes.

## Detection Output

| Field | Description |
|---|---|
| `host` | Linux system receiving the authentication activity |
| `src_ip` | Source IP address generating the attempts |
| `username` | Account targeted by the activity |
| `failed_attempts` | Total number of failed password attempts |
| `first_failure` | Time of the first failed attempt |
| `last_failure` | Time of the latest failed attempt |
| `successful_login_time` | Time of the successful authentication |
| `attack_window_seconds` | Time between the first failure and successful login |
| `time_after_last_failure_seconds` | Time between the final failure and successful login |

## Validated Test Result

The detection was validated inside the Mini SOC lab.

| Field | Validated Result |
|---|---|
| Destination host | `victim` |
| Source IP | `192.168.56.30` |
| Targeted account | `soc-test` |
| Failed attempts | `5` |
| First failure | `2026-07-19 21:51:33 +03:00` |
| Last failure | `2026-07-19 21:51:39 +03:00` |
| Successful login | `2026-07-19 21:51:46 +03:00` |
| Attack window | Approximately `12.69` seconds |
| Time after final failure | Approximately `6.49` seconds |

## Alert Configuration

| Setting | Value |
|---|---|
| Alert name | `SSH Brute Force Followed by Successful Login` |
| Alert type | Scheduled |
| Schedule | Every 5 minutes |
| Cron expression | `*/5 * * * *` |
| Search time range | Last 10 minutes |
| Trigger condition | Number of results is greater than `0` |
| Trigger mode | Once |
| Severity | High |
| Trigger action | Add to Triggered Alerts |

## Why High Severity Was Selected

High severity was selected because the detection confirms that a successful SSH password authentication occurred after repeated failed attempts.

This sequence represents a stronger indication of possible account compromise than failed login attempts alone.

The severity should be increased to Critical when additional evidence is observed, such as:

- The account has administrative privileges
- The successful login targets the `root` account
- Privilege escalation occurs after login
- Persistence is established
- Sensitive files are accessed
- Suspicious commands are executed
- Additional systems are targeted

## Investigation Steps

1. Confirm the source IP address.
2. Confirm the targeted username.
3. Review the total number of failed attempts.
4. Confirm that the successful login occurred after the failures.
5. Review the complete SSH session.
6. Search for commands executed after login.
7. Check for `sudo`, `su`, or privilege-escalation activity.
8. Review processes and network connections created by the account.
9. Check whether the source IP targeted other systems.
10. Determine whether the login was authorized.
11. Preserve relevant logs and investigation evidence.
12. Document the final classification and response actions.

## Potential False Positives

- A legitimate user repeatedly entering an incorrect password before remembering it
- An administrator using outdated credentials
- A password-management or automation issue
- An authorized penetration test
- A security validation exercise
- A user changing a password and continuing to use the previous password temporarily

## Recommended Response Actions

- Confirm whether the login was authorized
- Isolate the affected account when compromise is suspected
- Terminate active SSH sessions
- Reset the account password
- Revoke exposed credentials or SSH keys
- Block or restrict the source IP address
- Review commands executed after authentication
- Search for privilege escalation and persistence
- Review other systems for related authentication activity
- Preserve logs and forensic evidence

## MITRE ATT&CK Mapping

| Category | Mapping |
|---|---|
| Tactic | Credential Access (`TA0006`) |
| Technique | Brute Force (`T1110`) |
| Sub-technique | Password Guessing (`T1110.001`) |
| Platform | Linux |
| Targeted service | SSH (`22/TCP`) |

## Search Window Requirement

This detection is designed for a limited rolling search window such as:

```text
Last 10 minutes
```

Running the query over `All time` may combine unrelated historical authentication attempts for the same host, source IP, and username.

Historical analysis requires separate sessionization or time-bucketing logic to isolate each failure-to-success sequence.

## Limitations

This detection may not independently identify:

- Successful authentication using SSH keys
- Distributed attacks from multiple source IP addresses
- Low-and-slow attacks below the configured threshold
- Password attempts spread across several usernames
- Activity stored in another index or log source
- Post-authentication actions performed outside the search window

## Safety Notice

All authentication activity used to validate this detection was generated inside an isolated and authorized Mini SOC lab environment.
