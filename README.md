# Mini SOC Monitoring Lab with Splunk

## Overview

This project documents a hands-on Mini SOC lab built to practice SOC monitoring, Splunk-based detection, alerting, dashboards, log analysis, IOC extraction, alert investigation, and incident documentation.

The current detection use cases focus on:

- Detecting repeated SSH authentication failures
- Correlating failed SSH attempts followed by successful authentication
- Detecting successful SSH access followed by sudo execution and root-level privilege escalation

## Lab Environment

| Component | Operating System | Role |
|---|---|---|
| Splunk Server | Ubuntu Server 22.04 | Centralized log collection, analysis, alerts, and dashboards |
| Victim Machine | Linux | Monitored target that generates authentication logs |
| Kali Linux | Kali Linux | Controlled attack simulation machine |

## Tools Used

- Splunk Enterprise
- Splunk Universal Forwarder
- Ubuntu Server
- Kali Linux
- Linux authentication logs
- SPL
- Hydra
- SSH
- sudo
- Fail2Ban
- VirtualBox

## Detection Use Cases

### 1. SSH Brute Force Detection

This detection identifies repeated failed SSH login attempts originating from the same source IP address within a short time window.

| Setting | Value |
|---|---|
| Failure threshold | 5 attempts |
| Search window | Last 5 minutes |
| Severity | Medium |
| Validation result | Triggered successfully |

### 2. SSH Brute Force Followed by Successful Login

This detection correlates repeated failed SSH password attempts with a subsequent successful login from the same source IP address and against the same account.

| Setting | Value |
|---|---|
| Failure threshold | 5 attempts |
| Correlation window | Last 10 minutes |
| Severity | High |
| Validation result | Triggered successfully |

### 3. SSH Successful Login Followed by Privilege Escalation

This detection correlates a successful SSH password login with subsequent sudo command execution and the opening of a root session for the same Linux account.

| Setting | Value |
|---|---|
| Correlation sequence | SSH login → sudo command → root session |
| Internal correlation limit | 600 seconds |
| Scheduled search range | Last 15 minutes |
| Schedule | Every 5 minutes |
| Severity | Critical |
| Throttle | 15 minutes |
| Validation result | Triggered successfully |

## MITRE ATT&CK Mapping

| Use Case | Tactic | Technique | Sub-technique |
|---|---|---|---|
| SSH Brute Force Detection | Credential Access (`TA0006`) | Brute Force (`T1110`) | Password Guessing (`T1110.001`) |
| SSH Brute Force Followed by Successful Login | Credential Access (`TA0006`) | Brute Force (`T1110`) | Password Guessing (`T1110.001`) |
| SSH Login Followed by Privilege Escalation | Privilege Escalation (`TA0004`) | Abuse Elevation Control Mechanism (`T1548`) | Sudo and Sudo Caching (`T1548.003`) |

Related techniques for the third use case:

- Remote Services: SSH (`T1021.004`)
- Valid Accounts: Local Accounts (`T1078.003`)

## Project Contents

- Mini SOC lab architecture
- Lab setup guide
- Centralized Linux log collection
- SPL detection and correlation queries
- Scheduled alert configurations
- SSH brute-force simulation
- Failure-to-success authentication correlation
- SSH-to-root privilege-escalation correlation
- Positive and negative detection testing
- Alert throttling and duplicate suppression
- Alert investigation and IOC extraction
- SOC-style incident reports
- MITRE ATT&CK mapping
- SOC monitoring dashboard
- Validation screenshots
- Lessons learned

## What I Learned

- Collecting and analyzing Linux authentication logs
- Configuring Splunk Universal Forwarder
- Writing SPL queries for SSH detections
- Extracting fields from raw events using `rex`
- Handling compressed `message repeated` events
- Correlating failed and successful authentication events
- Correlating SSH, sudo, and root-session events
- Using `streamstats` to preserve chronological event context
- Returning separate results for independent escalation sequences
- Creating scheduled Splunk alerts
- Assigning severity based on detection context
- Testing detections using positive and negative scenarios
- Preventing duplicate alerts using throttling
- Investigating alerts and extracting indicators
- Reviewing successful authentication after repeated failures
- Investigating root-level command execution
- Creating SOC monitoring dashboards
- Writing SOC-style incident reports
- Mapping detections to MITRE ATT&CK
- Testing queries manually before configuring alerts

## Disclaimer

This project was built in a controlled and isolated lab environment for educational and portfolio purposes only.

All authentication, privilege-escalation, and attack-simulation activity was performed against systems owned by the tester. No public, production, or unauthorized systems were targeted.

## Repository Structure

```text
mini-soc-splunk-lab/
├── README.md
├── detections/
│   ├── ssh-bruteforce-detection.spl
│   ├── ssh-bruteforce-followed-by-success.spl
│   └── ssh-login-followed-by-privilege-escalation.spl
├── reports/
│   ├── ssh-bruteforce-incident-report.md
│   ├── ssh-bruteforce-followed-by-success-incident-report.md
│   └── ssh-login-followed-by-privilege-escalation-incident-report.md
├── docs/
│   ├── alert-configuration.md
│   ├── architecture.md
│   ├── lessons-learned.md
│   ├── setup-guide.md
│   ├── ssh-bruteforce-use-case.md
│   ├── ssh-bruteforce-followed-by-success-use-case.md
│   ├── ssh-bruteforce-followed-by-success-alert-configuration.md
│   ├── ssh-login-followed-by-privilege-escalation-use-case.md
│   └── ssh-login-followed-by-privilege-escalation-alert-configuration.md
└── screenshots/
    ├── 01-lab-virtual-machines.png
    ├── 02-splunk-log-ingestion.png
    ├── 03-ssh-bruteforce-events.png
    ├── 04-detection-query-results.png
    ├── 05-alert-configuration.png
    ├── 06-triggered-alert.png
    ├── 07-soc-dashboard.png
    ├── 08-investigation-evidence.png
    ├── 09-ssh-failure-success-events.png
    ├── 10-ssh-failure-success-detection-results.png
    ├── 11-ssh-privilege-escalation-detection-results.png
    ├── 12-ssh-privilege-escalation-triggered-alert.png
    └── README.md
```

## Documentation

### Lab Documentation

- [Lab Architecture](docs/architecture.md)
- [Lab Setup Guide](docs/setup-guide.md)
- [Lessons Learned](docs/lessons-learned.md)

### SSH Brute-Force Detection

- [SSH Brute-Force Detection Use Case](docs/ssh-bruteforce-use-case.md)
- [SSH Brute-Force Alert Configuration](docs/alert-configuration.md)
- [SSH Brute-Force Detection Query](detections/ssh-bruteforce-detection.spl)
- [SSH Brute-Force Incident Report](reports/ssh-bruteforce-incident-report.md)

### SSH Failure-to-Success Detection

- [SSH Failure-to-Success Detection Use Case](docs/ssh-bruteforce-followed-by-success-use-case.md)
- [SSH Failure-to-Success Alert Configuration](docs/ssh-bruteforce-followed-by-success-alert-configuration.md)
- [SSH Failure-to-Success Detection Query](detections/ssh-bruteforce-followed-by-success.spl)
- [SSH Failure-to-Success Incident Report](reports/ssh-bruteforce-followed-by-success-incident-report.md)

### SSH Privilege-Escalation Detection

- [SSH Privilege-Escalation Detection Use Case](docs/ssh-login-followed-by-privilege-escalation-use-case.md)
- [SSH Privilege-Escalation Alert Configuration](docs/ssh-login-followed-by-privilege-escalation-alert-configuration.md)
- [SSH Privilege-Escalation Detection Query](detections/ssh-login-followed-by-privilege-escalation.spl)
- [SSH Privilege-Escalation Incident Report](reports/ssh-login-followed-by-privilege-escalation-incident-report.md)

### Evidence

- [Project Screenshots and Validation Evidence](screenshots/README.md)

## Visual Evidence

The following dashboard provides an overview of the security events monitored inside the Mini SOC lab.

![SOC Monitoring Dashboard](screenshots/07-soc-dashboard.png)

The complete validation gallery includes:

- Virtual lab architecture
- Linux log ingestion
- Raw SSH authentication events
- SPL detection results
- Alert configurations
- Triggered alerts
- Investigation evidence
- Failure-to-success authentication correlation
- SSH login followed by privilege escalation
- Critical alert and throttle validation

[View the complete evidence gallery](screenshots/README.md)

## Validated Results

### SSH Brute-Force Detection

| Field | Result |
|---|---|
| Destination host | `victim` |
| Source IP | `192.168.56.30` |
| Targeted user | `saeed` |
| Failed attempts | `6` |
| Severity | Medium |
| Alert status | Triggered successfully |

### SSH Brute Force Followed by Successful Login

| Field | Result |
|---|---|
| Destination host | `victim` |
| Source IP | `192.168.56.30` |
| Targeted account | `soc-test` |
| Failed attempts | `5` |
| Attack window | Approximately `12.69` seconds |
| Time after final failure | Approximately `6.49` seconds |
| Severity | High |
| Alert status | Triggered successfully |

### SSH Successful Login Followed by Privilege Escalation

| Field | Result |
|---|---|
| Destination host | `victim` |
| Source IP | `192.168.56.30` |
| Authenticated account | `soc-test` |
| Privileged account | `root` |
| Executed command | `/usr/bin/id` |
| First validated time to root | Approximately `11.43` seconds |
| Second validated time to root | Approximately `5.68` seconds |
| Severity | Critical |
| Alert status | Triggered successfully |
| Duplicate suppression | Verified using a 15-minute throttle |

## Validation Matrix

| Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|
| Repeated failed SSH passwords | Medium alert | Medium alert | Passed |
| Failed SSH attempts followed by successful login | High alert | High alert | Passed |
| SSH login without sudo | No privilege-escalation detection | No detection | Passed |
| Local sudo without SSH login | No SSH privilege-escalation detection | No detection | Passed |
| SSH login followed by sudo and root session | Critical alert | Critical alert | Passed |
| Multiple privilege-escalation sequences | Separate results | Separate results | Passed |
| Repeated scheduled searches | Duplicate alerts suppressed | Suppressed | Passed |

## Current Project Status

Three SSH detection use cases have been implemented, tested, investigated, validated, and documented.

Completed items:

- Mini SOC lab setup guide
- Virtual lab architecture
- Centralized Linux log collection
- Splunk Universal Forwarder configuration
- SSH brute-force simulation
- SSH brute-force detection query
- SSH failure-to-success correlation query
- SSH privilege-escalation correlation query
- Medium-severity brute-force alert
- High-severity compromise-pattern alert
- Critical privilege-escalation alert
- Positive and negative validation testing
- Multiple-sequence correlation testing
- Scheduled alert validation
- Triggered alert verification
- Fifteen-minute alert throttling
- Duplicate-alert suppression validation
- Alert investigation
- IOC extraction
- Three SOC-style incident reports
- MITRE ATT&CK mapping
- SOC monitoring dashboard
- Visual evidence gallery
- Lessons learned documentation

Additional detection use cases will be added only after they are configured, tested, investigated, and validated inside the lab.
