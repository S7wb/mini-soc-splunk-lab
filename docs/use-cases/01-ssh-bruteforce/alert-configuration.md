# SSH Brute-Force Alert Configuration

## Overview

This document describes the Splunk alert configuration used for the validated SSH brute-force detection in the Mini SOC lab.

The alert monitors Linux authentication logs and triggers when five or more failed SSH login attempts originate from the same source IP address during a five-minute search window.

## Alert Details

| Setting | Value |
|---|---|
| Alert Name | `SSH Brute Force Detection` |
| Alert Type | Scheduled |
| Schedule | Every 5 minutes |
| Cron Expression | `*/5 * * * *` |
| Search Time Range | Last 5 minutes |
| Trigger Condition | Number of results is greater than `0` |
| Trigger Mode | Once |
| Trigger Action | Add to Triggered Alerts |
| Severity | Medium |
| Throttle | Disabled |
| Display Mode | Digest |

## Detection Query

The alert uses the validated SPL query stored in:

```text
detections/ssh-bruteforce-detection.spl
```

The query:

1. Searches Linux authentication logs for failed SSH passwords.
2. Extracts the source IP address and targeted username.
3. Handles compressed `message repeated` events.
4. Calculates the total number of failed attempts.
5. Groups the activity by monitored host and source IP.
6. Returns a result when five or more failed attempts are detected.

## Validated Alert Test

The alert was tested by generating controlled failed SSH authentication attempts from Kali Linux using Hydra.

| Field | Validated Result |
|---|---|
| Alert Status | Triggered successfully |
| Alert Time | `2026-07-19 17:05:01 +03:00` |
| Destination Host | `victim` |
| Source IP | `192.168.56.30` |
| Targeted User | `saeed` |
| Failed Attempts | `6` |
| First Seen | Approximately `2026-07-19 17:01:56 +03:00` |
| Last Seen | Approximately `2026-07-19 17:02:11 +03:00` |
| Activity Duration | Approximately `14.76` seconds |
| Severity | Medium |

The alert appeared successfully in the Splunk **Triggered Alerts** page after the next scheduled execution.

## Alert Workflow

1. Failed SSH login attempts are recorded in `/var/log/auth.log`.
2. Splunk Universal Forwarder sends the events to Splunk Enterprise.
3. The scheduled alert runs every five minutes.
4. The search reviews events from the previous five minutes.
5. The SPL query calculates failed attempts by source IP and destination host.
6. A result is returned when the threshold is reached.
7. Splunk adds the alert to the Triggered Alerts page with Medium severity.
8. The analyst reviews the detection results and begins investigation.

## Why Medium Severity Was Selected

Medium severity was selected because this alert detects failed authentication attempts without confirming that unauthorized access succeeded.

The severity should be increased when additional evidence is present, such as:

- A successful SSH login after repeated failures
- Authentication to a privileged account
- Suspicious commands after login
- Privilege escalation
- Persistence activity
- Connections from a known malicious source

## Recommended Production Tuning

The following settings may need adjustment in another environment:

| Setting | Tuning Consideration |
|---|---|
| Threshold | Increase or decrease based on normal authentication behavior |
| Search window | Adjust for rapid or low-and-slow password attacks |
| Schedule | Align with the selected search window |
| Severity | Increase when successful compromise indicators are present |
| Throttling | Enable when duplicate alerts create excessive noise |
| Allowlisting | Exclude approved scanners or administration systems when justified |

## Validation Status

The alert configuration has been:

- Configured in Splunk Enterprise
- Tested using controlled Hydra activity
- Triggered successfully
- Verified in the Triggered Alerts page
- Confirmed to display the expected detection fields

## Safety Notice

The authentication activity used to validate this alert was generated only inside an isolated and authorized Mini SOC lab environment.
