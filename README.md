# Mini SOC Monitoring Lab with Splunk

## Overview

This project presents a hands-on Mini SOC Monitoring Lab built with Splunk to simulate real-world security monitoring and incident investigation workflows. The lab focuses on centralized log collection, detection engineering, alerting, event correlation, IOC extraction, incident investigation, MITRE ATT&CK mapping, and SOC-style incident documentation.

The environment consists of an Ubuntu-based Splunk server, an Ubuntu victim machine, and a Kali Linux attacker machine operating inside an isolated VirtualBox lab network.

The current detection use cases focus on:

- Detecting repeated SSH authentication failures
- Correlating failed SSH attempts followed by successful authentication
- Detecting successful SSH access followed by sudo execution and root-level privilege escalation
- Detecting repeated failed sudo authentication attempts

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
- Docker
- n8n
- Webhooks
- Telegram Bot

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

### 4. Multiple Failed sudo Attempts

This detection identifies repeated failed `sudo` authentication attempts on a Linux host and alerts when three or more incorrect sudo password attempts are recorded.

| Setting | Value |
|---|---|
| Failure threshold | 3 incorrect sudo password attempts |
| Search window | Last 5 minutes |
| Schedule | Every 5 minutes |
| Severity | Medium |
| Validation result | Triggered successfully |
| Privilege-escalation outcome | No successful sudo session observed |

## MITRE ATT&CK Mapping

| Use Case | Tactic | Technique | Sub-technique |
|---|---|---|---|
| SSH Brute Force Detection | Credential Access (`TA0006`) | Brute Force (`T1110`) | Password Guessing (`T1110.001`) |
| SSH Brute Force Followed by Successful Login | Credential Access (`TA0006`) | Brute Force (`T1110`) | Password Guessing (`T1110.001`) |
| SSH Login Followed by Privilege Escalation | Privilege Escalation (`TA0004`) | Abuse Elevation Control Mechanism (`T1548`) | Sudo and Sudo Caching (`T1548.003`) |
| Multiple Failed sudo Attempts | Privilege Escalation (`TA0004`) | Abuse Elevation Control Mechanism (`T1548`) | Sudo and Sudo Caching (`T1548.003`) |

Related techniques for the third use case:

- Remote Services: SSH (`T1021.004`)
- Valid Accounts: Local Accounts (`T1078.003`)

## SOC Alert Automation

The Mini SOC lab also includes a validated security automation workflow that extends Splunk alerting with automated analyst notification.

The automation uses **n8n** to receive triggered Splunk alerts through a webhook, reduce duplicate processing, and deliver structured SOC notifications through Telegram.

### Automation Architecture

```text
Linux Security Event
        |
        v
Splunk Universal Forwarder
        |
        v
Splunk Enterprise
        |
        v
SPL Detection
        |
        v
Scheduled Alert
        |
        v
Splunk Webhook Alert Action
        |
        v
n8n Webhook
        |
        v
Remove Duplicates
        |
        v
Telegram Bot
        |
        v
SOC Analyst Notification
```

### Validated Automation

The first detection integrated with the automation workflow is:

**SSH Brute-Force Detection**

The end-to-end workflow was successfully validated:

| Stage | Status |
|---|---|
| Splunk detection | Validated |
| Scheduled alert | Validated |
| Webhook alert action | Validated |
| n8n webhook reception | Validated |
| Duplicate filtering | Validated |
| Telegram execution | Validated |
| Analyst notification | Validated |

The automation extends the original SOC workflow from:

```text
Detection → Alert → Manual Review
```

to:

```text
Detection → Alert → Automation → Notification → Investigation
```

### Automation Workflow

The implemented n8n workflow contains:

```text
Webhook
   |
   v
Remove Duplicates
   |
   v
Telegram
```

A sanitized version of the workflow is available for review and import:

- [Sanitized n8n Workflow](automation/workflows/ssh-bruteforce-telegram.json)

### Automation Documentation

- [SOC Alert Automation Overview](automation/README.md)
- [n8n Installation](automation/n8n-installation.md)
- [Splunk Webhook Integration](automation/splunk-webhook-integration.md)
- [n8n Workflow Design](automation/workflow-design.md)
- [Telegram Integration](automation/telegram-integration.md)
- [End-to-End Validation](automation/validation.md)

### Automation Evidence

The repository includes screenshots demonstrating:

- n8n running inside Docker
- n8n web interface availability
- Splunk Webhook alert action
- Successful Splunk-to-n8n webhook reception
- Successful n8n workflow execution
- Duplicate filtering
- Successful Telegram node execution
- Final SOC alert delivered to Telegram

[View the complete evidence gallery](screenshots/README.md)

> Sensitive credentials, Telegram tokens, Chat IDs, webhook identifiers, and environment-specific IDs were removed or redacted before publication.

## Project Contents

- Mini SOC lab architecture
- Lab setup guide
- Centralized Linux log collection
- SPL detection and correlation queries
- Scheduled alert configurations
- SSH brute-force simulation
- Failure-to-success authentication correlation
- SSH-to-root privilege-escalation correlation
- Multiple failed sudo authentication detection
- sudo authentication failure investigation
- Positive and negative detection testing
- Alert throttling and duplicate suppression
- Alert investigation and IOC extraction
- SOC-style incident reports
- MITRE ATT&CK mapping
- SOC monitoring dashboard
- Validation screenshots
- Lessons learned
- Splunk-to-n8n webhook integration
- n8n SOC alert automation workflow
- Duplicate alert processing control
- Telegram analyst notifications
- End-to-end automation validation
- Sanitized reusable n8n workflow template

## What I Learned

- Collecting and analyzing Linux authentication logs
- Configuring Splunk Universal Forwarder
- Writing SPL queries for SSH detections
- Extracting fields from raw events using `rex`
- Handling compressed `message repeated` events
- Correlating failed and successful authentication events
- Correlating SSH, sudo, and root-session events
- Detecting repeated failed sudo authentication attempts
- Extracting sudo failure counts from Linux authentication logs using SPL
- Investigating whether failed sudo attempts were followed by a successful privileged session
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
- Integrating Splunk alerts with external automation platforms
- Using webhooks for SIEM alert orchestration
- Building security automation workflows with n8n
- Reducing duplicate automated notifications
- Delivering structured SOC alerts through Telegram
- Separating SIEM detection from notification automation
- Sanitizing automation workflows before publishing them publicly

## Disclaimer

This project was built in a controlled and isolated lab environment for educational and portfolio purposes only.

All authentication, privilege-escalation, and attack-simulation activity was performed against systems owned by the tester. No public, production, or unauthorized systems were targeted.

## Repository Structure

```text
mini-soc-splunk-lab/
├── README.md
├── automation/
│   ├── README.md
│   ├── n8n-installation.md
│   ├── splunk-webhook-integration.md
│   ├── workflow-design.md
│   ├── telegram-integration.md
│   ├── validation.md
│   └── workflows/
│       └── ssh-bruteforce-telegram.json
├── detections/
│   ├── 01-ssh-bruteforce.spl
│   ├── 02-ssh-failure-to-success.spl
│   ├── 03-ssh-privilege-escalation.spl
│   └── 04-multiple-failed-sudo-attempts.spl
├── reports/
│   ├── 01-ssh-bruteforce-incident-report.md
│   ├── 02-ssh-failure-to-success-incident-report.md
│   ├── 03-ssh-privilege-escalation-incident-report.md
│   └── 04-multiple-failed-sudo-attempts-incident-report.md
├── docs/
│   ├── lab/
│   │   ├── architecture.md
│   │   ├── setup-guide.md
│   │   └── lessons-learned.md
│   └── use-cases/
│       ├── 01-ssh-bruteforce/
│       │   ├── use-case.md
│       │   └── alert-configuration.md
│       ├── 02-ssh-failure-to-success/
│       │   ├── use-case.md
│       │   └── alert-configuration.md
│       ├── 03-ssh-privilege-escalation/
│       │   ├── use-case.md
│       │   └── alert-configuration.md
│       └── 04-multiple-failed-sudo-attempts/
│           ├── use-case.md
│           └── alert-configuration.md
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
    ├── 13-n8n-container-running.png
    ├── 14-n8n-web-interface.png
    ├── 15-splunk-webhook-action.png
    ├── 16-n8n-webhook-received.png
    ├── 17-n8n-workflow-execution.png
    ├── 18-n8n-remove-duplicates.png
    ├── 19-n8n-telegram-execution.png
    ├── 20-telegram-soc-alert.png
    ├── 04-multiple-failed-sudo-attempts/
    │   ├── 01-sudo-failed-attempts.png
    │   ├── 02-raw-sudo-event-splunk.png
    │   ├── 03-spl-detection-result.png
    │   ├── 04-detection-threshold-validation.png
    │   ├── 05-alert-configuration.png
    │   ├── 06-alert-saved-successfully.png
    │   ├── 07-triggered-alert.png
    │   ├── 08-triggered-alert-result.png
    │   ├── 09-sudo-authentication-investigation.png
    │   └── 10-no-successful-sudo-session.png
    └── README.md
```

## Documentation

### Lab Documentation

- [Lab Architecture](docs/lab/architecture.md)
- [Lab Setup Guide](docs/lab/setup-guide.md)
- [Lessons Learned](docs/lab/lessons-learned.md)

### SSH Brute-Force Detection

- [SSH Brute-Force Detection Use Case](docs/use-cases/01-ssh-bruteforce/use-case.md)
- [SSH Brute-Force Alert Configuration](docs/use-cases/01-ssh-bruteforce/alert-configuration.md)
- [SSH Brute-Force Detection Query](detections/01-ssh-bruteforce.spl)
- [SSH Brute-Force Incident Report](reports/01-ssh-bruteforce-incident-report.md)

### SSH Failure-to-Success Detection

- [SSH Failure-to-Success Detection Use Case](docs/use-cases/02-ssh-failure-to-success/use-case.md)
- [SSH Failure-to-Success Alert Configuration](docs/use-cases/02-ssh-failure-to-success/alert-configuration.md)
- [SSH Failure-to-Success Detection Query](detections/02-ssh-failure-to-success.spl)
- [SSH Failure-to-Success Incident Report](reports/02-ssh-failure-to-success-incident-report.md)

### SSH Privilege-Escalation Detection

- [SSH Privilege-Escalation Detection Use Case](docs/use-cases/03-ssh-privilege-escalation/use-case.md)
- [SSH Privilege-Escalation Alert Configuration](docs/use-cases/03-ssh-privilege-escalation/alert-configuration.md)
- [SSH Privilege-Escalation Detection Query](detections/03-ssh-privilege-escalation.spl)
- [SSH Privilege-Escalation Incident Report](reports/03-ssh-privilege-escalation-incident-report.md)

### Multiple Failed sudo Attempts

- [Multiple Failed sudo Attempts Use Case](docs/use-cases/04-multiple-failed-sudo-attempts/use-case.md)
- [Multiple Failed sudo Attempts Alert Configuration](docs/use-cases/04-multiple-failed-sudo-attempts/alert-configuration.md)
- [Multiple Failed sudo Attempts Detection Query](detections/04-multiple-failed-sudo-attempts.spl)
- [Multiple Failed sudo Attempts Incident Report](reports/04-multiple-failed-sudo-attempts-incident-report.md)

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

### Multiple Failed sudo Attempts

| Field | Result |
|---|---|
| Destination host | `victim` |
| User | `saeed` |
| Failed sudo attempts | `3` |
| Requested privileged account | `root` |
| Attempted command | `/usr/bin/whoami` |
| Detection threshold | `failed_attempts >= 3` |
| Search window | Last 5 minutes |
| Schedule | Every 5 minutes |
| Severity | Medium |
| Alert status | Triggered successfully |
| Successful sudo session | Not observed |
| Privilege escalation outcome | Not successful |

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
| Three failed sudo password attempts | Medium alert | Medium alert | Passed |
| Failed sudo attempts followed by no successful root session | No successful privilege escalation | No successful privilege escalation | Passed |

## Current Project Status

Four detection use cases have been implemented, tested, investigated, validated, and documented.

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
- Four SOC-style incident reports
- MITRE ATT&CK mapping
- SOC monitoring dashboard
- Visual evidence gallery
- Lessons learned documentation
- Splunk-to-n8n webhook integration
- n8n SOC alert automation workflow
- Duplicate alert processing control
- Telegram SOC notification integration
- End-to-end automation validation
- Sanitized n8n workflow published for portfolio review
- Multiple failed sudo attempts detection
- Medium-severity sudo authentication alert
- sudo authentication investigation
- Validation of no successful sudo/root session
Additional detection use cases will be added only after they are configured, tested, investigated, and validated inside the lab.
