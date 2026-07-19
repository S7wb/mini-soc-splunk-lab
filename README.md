# Mini SOC Monitoring Lab with Splunk

## Overview

This project documents a hands-on Mini SOC lab built to practice SOC monitoring, Splunk-based detection, alerting, dashboards, log analysis, IOC extraction, alert investigation, and incident documentation.

The current detection use cases focus on identifying SSH brute-force activity and detecting repeated failed SSH password attempts followed by successful authentication.

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

## MITRE ATT&CK Mapping

| Category | Mapping |
|---|---|
| Tactic | Credential Access (`TA0006`) |
| Technique | Brute Force (`T1110`) |
| Sub-technique | Password Guessing (`T1110.001`) |
| Platform | Linux |
| Targeted Service | SSH (`22/TCP`) |

## Project Contents

- Mini SOC lab architecture
- Lab setup guide
- Centralized Linux log collection
- SPL detection queries
- Scheduled alert configurations
- SSH brute-force simulation
- Failure-to-success authentication correlation
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
- Creating scheduled Splunk alerts
- Assigning severity based on detection context
- Investigating alerts and extracting indicators
- Reviewing successful authentication after repeated failures
- Creating SOC monitoring dashboards
- Writing SOC-style incident reports
- Mapping detections to MITRE ATT&CK
- Testing queries manually before configuring alerts

## Disclaimer

This project was built in a controlled and isolated lab environment for educational and portfolio purposes only.

All authentication and attack-simulation activity was performed against systems owned by the tester. No public, production, or unauthorized systems were targeted.

## Repository Structure

```text
mini-soc-splunk-lab/
├── README.md
├── detections/
│   ├── ssh-bruteforce-detection.spl
│   └── ssh-bruteforce-followed-by-success.spl
├── reports/
│   ├── ssh-bruteforce-incident-report.md
│   └── ssh-bruteforce-followed-by-success-incident-report.md
├── docs/
│   ├── alert-configuration.md
│   ├── architecture.md
│   ├── lessons-learned.md
│   ├── setup-guide.md
│   ├── ssh-bruteforce-use-case.md
│   ├── ssh-bruteforce-followed-by-success-use-case.md
│   └── ssh-bruteforce-followed-by-success-alert-configuration.md
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
- Alert configuration
- Triggered alerts
- Investigation evidence
- Failure-to-success authentication correlation

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

## Current Project Status

Two SSH detection use cases have been implemented, tested, validated, and documented.

Completed items:

- Mini SOC lab setup guide
- Virtual lab architecture
- Centralized Linux log collection
- Splunk Universal Forwarder configuration
- SSH brute-force simulation
- SSH brute-force detection query
- SSH failure-to-success correlation query
- Medium-severity brute-force alert
- High-severity compromise-pattern alert
- Scheduled alert validation
- Triggered alert verification
- Alert investigation
- IOC extraction
- Two SOC-style incident reports
- MITRE ATT&CK mapping
- SOC monitoring dashboard
- Visual evidence gallery
- Lessons learned documentation

Additional detection use cases will be added only after they are configured, tested, investigated, and validated inside the lab.
