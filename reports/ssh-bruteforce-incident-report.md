# SSH Brute-Force Incident Report

## Incident Summary

A simulated SSH brute-force attack was detected against the Linux host `victim` in the Mini SOC lab.

Six failed SSH authentication attempts targeting the user `saeed` originated from the same source IP address within approximately 14.78 seconds.

The activity was generated from Kali Linux using Hydra inside an authorized and isolated lab environment.

## Alert Details

| Field | Value |
|---|---|
| Alert Name | SSH Brute-Force Detection |
| Detection Status | Triggered |
| Classification | True Positive — Authorized Simulation |
| Severity | Medium |
| Incident Status | Closed |
| Destination Host | `victim` |
| Source IP | `192.168.56.30` |
| Targeted User | `saeed` |
| Targeted Service | SSH |
| Destination Port | `22` |
| Failed Attempts | `6` |
| Activity Duration | Approximately `14.78` seconds |
| First Seen | `2026-07-19 15:06:38 +03:00` |
| Last Seen | `2026-07-19 15:06:53 +03:00` |

## Data Source

| Field | Value |
|---|---|
| Splunk Index | `main` |
| Log Source | `/var/log/auth.log` |
| Service Process | `sshd` |
| Monitored Host | `victim` |

## Detection Logic

The detection searches for Linux SSH events containing:

```text
Failed password
```

It extracts the source IP address and targeted username, calculates repeated events recorded as `message repeated`, and groups the activity by destination host and source IP.

The detection triggers when the same source IP generates five or more failed SSH login attempts during the configured search window.

The validated SPL query is stored in:

```text
detections/ssh-bruteforce-detection.spl
```

## Key Evidence

- Six incorrect passwords were tested using Hydra.
- All attempts targeted the account `saeed`.
- All attempts originated from `192.168.56.30`.
- The destination system was `victim`.
- The attempts occurred within approximately 14.78 seconds.
- Linux authentication logs recorded the failed SSH activity.
- Splunk correctly extracted and aggregated the related events.
- Hydra reported that no valid password was found.
- No successful SSH login was observed during the test.

## Extracted Indicators

| Indicator Type | Value | Description |
|---|---|---|
| Source IP | `192.168.56.30` | Kali Linux attack simulation host |
| Destination Host | `victim` | Monitored Linux system |
| Targeted User | `saeed` | Account targeted during the simulation |
| Service | `SSH` | Targeted remote-access service |
| Destination Port | `22` | Default SSH service port |
| Authentication Result | Failed | No valid password was identified |

> The source IP is an internal lab address used for authorized testing and is not a real-world malicious IOC.

## Investigation Steps

1. Reviewed the failed authentication events in Splunk.
2. Confirmed that the events originated from the same source IP.
3. Identified the targeted username.
4. Calculated the total number of failed attempts.
5. Reviewed the first and last event timestamps.
6. Confirmed that the activity targeted the SSH service.
7. Checked whether a successful login followed the failed attempts.
8. Confirmed that Hydra did not identify a valid password.
9. Classified the alert as a true positive caused by authorized simulation.
10. Documented the evidence and recommended response actions.

## Assessment

The activity matched the defined SSH brute-force detection conditions.

Because the source IP generated six failed authentication attempts against the same account in less than 15 seconds, the alert represents a high-confidence password-guessing pattern.

No account compromise occurred during the test because no successful authentication was observed.

## Recommended Response Actions

In a production environment, the analyst should:

- Block or restrict the source IP if confirmed unauthorized.
- Review successful SSH logins from the same source IP.
- Review activity involving the targeted account.
- Temporarily lock or protect the targeted account when appropriate.
- Reset the password if compromise is suspected.
- Enforce strong authentication and consider SSH key-based access.
- Disable direct root SSH login where applicable.
- Implement rate limiting or Fail2ban.
- Review other systems for related authentication activity.
- Preserve relevant logs and investigation evidence.

## Closure

The incident was closed as authorized simulated activity after confirming that:

- The attack was intentionally generated inside the Mini SOC lab.
- The detection successfully identified the activity.
- No valid password was found.
- No successful login or account compromise occurred.

## Disclaimer

This incident report documents activity generated inside a controlled and authorized Mini SOC lab for educational and portfolio purposes only.
