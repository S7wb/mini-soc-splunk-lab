# SSH Brute Force Followed by Successful Login — Incident Report

## Incident Summary

A sequence of repeated failed SSH password attempts followed by a successful login was detected against the Linux host `victim` in the Mini SOC lab.

Five failed authentication attempts targeting the account `soc-test` originated from `192.168.56.30`. A successful SSH password login from the same source IP and account occurred approximately 6.49 seconds after the final failed attempt.

The activity was intentionally generated inside an isolated and authorized lab environment.

## Alert Details

| Field | Value |
|---|---|
| Alert Name | `SSH Brute Force Followed by Successful Login` |
| Detection Status | Triggered |
| Classification | True Positive — Authorized Simulation |
| Severity | High |
| Incident Status | Closed |
| Destination Host | `victim` |
| Source IP | `192.168.56.30` |
| Targeted Account | `soc-test` |
| Targeted Service | SSH |
| Destination Port | `22` |
| Failed Attempts | `5` |
| First Failure | `2026-07-19 21:51:33 +03:00` |
| Last Failure | `2026-07-19 21:51:39 +03:00` |
| Successful Login | `2026-07-19 21:51:46 +03:00` |
| Attack Window | Approximately `12.69` seconds |
| Time After Final Failure | Approximately `6.49` seconds |

## Data Source

| Field | Value |
|---|---|
| Splunk Index | `main` |
| Log Source | `/var/log/auth.log` |
| Service Process | `sshd` |
| Monitored Host | `victim` |

## Detection Logic

The detection correlates Linux SSH events containing:

```text
Failed password
```

and:

```text
Accepted password
```

It triggers when:

1. Five or more failed SSH password attempts are observed.
2. The attempts target the same username.
3. The attempts originate from the same source IP.
4. A successful password login occurs afterward.
5. The complete sequence occurs within ten minutes.

The validated SPL query is stored in:

```text
detections/ssh-bruteforce-followed-by-success.spl
```

## Key Evidence

- Five failed SSH password attempts targeted `soc-test`.
- All attempts originated from `192.168.56.30`.
- All events targeted the Linux host `victim`.
- A successful password authentication followed the failures.
- The successful login occurred 6.49 seconds after the last failure.
- The full failure-to-success sequence occurred within 12.69 seconds.
- Splunk correlated the events and triggered a High-severity alert.
- The authenticated session was validated using `whoami`.
- The resulting session ran under the `soc-test` account.

## Extracted Indicators

| Indicator Type | Value | Description |
|---|---|---|
| Source IP | `192.168.56.30` | Kali Linux simulation host |
| Destination Host | `victim` | Monitored Linux system |
| Targeted Account | `soc-test` | Account involved in the simulation |
| Service | SSH | Targeted remote-access service |
| Destination Port | `22` | Default SSH service port |
| Authentication Result | Successful after failures | Potential credential compromise pattern |

> The displayed source IP is an internal lab address used for authorized testing and is not a real-world malicious IOC.

## Investigation Steps

1. Reviewed the triggered High-severity Splunk alert.
2. Confirmed the destination host and source IP address.
3. Identified the targeted account.
4. Counted the failed password attempts.
5. Reviewed the first and last failed-event timestamps.
6. Confirmed that a successful login followed the failed attempts.
7. Verified that the source IP and username matched across the sequence.
8. Calculated the total attack window.
9. Calculated the delay between the final failure and successful login.
10. Reviewed the authenticated session.
11. Confirmed that the session operated as `soc-test`.
12. Determined whether the activity was authorized.
13. Documented the evidence and recommended response actions.

## Assessment

The activity matched the defined detection conditions for repeated SSH password failures followed by successful authentication.

In a production environment, this sequence would represent a strong indication that credentials may have been successfully guessed, obtained, or reused.

The incident was classified as a True Positive because the detection accurately identified the simulated failure-to-success authentication sequence.

No unauthorized compromise occurred because the activity was intentionally generated inside the controlled Mini SOC lab.

## Recommended Response Actions

In a production environment, the analyst should:

- Confirm whether the successful login was authorized.
- Temporarily lock or protect the affected account.
- Terminate suspicious SSH sessions.
- Reset the account password.
- Revoke exposed credentials or SSH keys.
- Block or restrict the source IP when confirmed unauthorized.
- Review commands executed after authentication.
- Search for `sudo`, `su`, and privilege-escalation activity.
- Check for persistence mechanisms.
- Review processes and network connections associated with the session.
- Search other systems for related authentication attempts.
- Preserve relevant logs and forensic evidence.

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
- The detection successfully correlated the failed and successful events.
- The scheduled alert triggered with High severity.
- The successful login used a dedicated non-administrative test account.
- No unauthorized production system or external target was involved.

## Disclaimer

This incident report documents controlled and authorized activity generated for educational and portfolio purposes only.
