# Mini SOC Monitoring Lab with Splunk

## Overview
This project documents a hands-on Mini SOC lab built to practice SOC monitoring, Splunk-based detection, alerting, dashboards, log analysis, and IOC extraction.

The main use case focuses on detecting SSH brute-force attempts using Linux authentication logs.

## Lab Environment

| Component | Operating System | Role |
|---|---|---|
| Splunk Server | Ubuntu Server 22.04 | Centralized log collection, analysis, alerts, and dashboards |
| Victim Machine | Linux | Monitored target that generates authentication logs |
| Kali Linux | Kali Linux | Controlled attack simulation machine |

## Tools Used
- Splunk
- Splunk Universal Forwarder
- Ubuntu Server
- Kali Linux
- Linux authentication logs
- SPL
- Hydra
- SSH

## Detection Use Case

### SSH Brute Force Detection

The detection identifies repeated failed SSH login attempts from the same source IP within a short time window.

## Project Contents
- Lab architecture
- SPL detection query
- Alerting logic
- SOC-style incident report
- Screenshots
- Lessons learned

## What I Learned
- Collecting and analyzing Linux authentication logs
- Writing SPL queries for brute-force detection
- Creating Splunk alerts and dashboards
- Investigating alerts and extracting IOCs
- Documenting SOC-style detection use cases

## Disclaimer
This project was built in a controlled lab environment for educational and portfolio purposes only.

## Repository Structure

```text
mini-soc-splunk-lab/
├── README.md
├── detections/
│   └── ssh-bruteforce-detection.spl
├── reports/
│   └── ssh-bruteforce-incident-report.md
├── docs/
│   ├── architecture.md
│   ├── lessons-learned.md
│   └── ssh-bruteforce-use-case.md
└── screenshots/
    └── README.md
```

## Documentation

- [Lab Architecture](docs/architecture.md)
- [SSH Brute-Force Detection Use Case](docs/ssh-bruteforce-use-case.md)
- [Lessons Learned](docs/lessons-learned.md)
- [SSH Brute-Force Detection Query](detections/ssh-bruteforce-detection.spl)
- [SSH Brute-Force Incident Report](reports/ssh-bruteforce-incident-report.md)
- [Project Screenshots](screenshots/README.md)

## Current Project Status

The SSH brute-force detection use case has been implemented, tested, and documented.

Completed items:

- Centralized Linux log collection
- SSH brute-force simulation
- SPL detection query
- Splunk alert configuration
- SOC monitoring dashboard
- Alert investigation
- IOC extraction
- Incident report
- Architecture documentation
- SSH brute-force use case documentation
- Lessons learned documentation
  
Additional detection use cases will be added after they are configured, tested, and validated in the lab.
