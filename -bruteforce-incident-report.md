# SSH Brute Force Incident Report

## Summary
A simulated SSH brute-force attack was detected against a Linux server in the Mini SOC lab. Multiple failed SSH login attempts were observed from the same source IP within a short time window.

## Alert Name
SSH Brute Force Detection

## Severity
Medium

## Affected Asset
Ubuntu Server

## Data Source
Linux authentication logs: `/var/log/auth.log`

## Detection Logic
The detection identifies repeated failed SSH login attempts from the same source IP.

## Evidence
- Multiple failed SSH authentication attempts
- Repeated login attempts from the same source IP
- Targeted usernames observed in authentication logs
- Activity detected using Splunk SPL

## Investigation Steps
1. Reviewed the triggered Splunk alert.
2. Identified the source IP address.
3. Counted the number of failed login attempts.
4. Reviewed targeted usernames.
5. Checked whether a successful login occurred after the failed attempts.
6. Extracted indicators of compromise.
7. Documented the incident in a SOC-style format.

## Extracted IOCs

| IOC Type | Value | Description |
|---|---|---|
| Source IP | x.x.x.x | Attacking host |
| Service | SSH | Targeted service |
| Port | 22 | SSH port |
| Usernames | root, admin, test | Attempted usernames |

## Recommended Actions
- Disable root SSH login.
- Enforce SSH key-based authentication.
- Block confirmed malicious source IPs.
- Review successful login events.
- Monitor for repeated failed login attempts.
- Apply account lockout or rate limiting where possible.

## Status
Closed as simulated lab activity.

## Disclaimer
This report was created as part of a controlled Mini SOC lab for educational and portfolio purposes.
