# Project Screenshots

[Project overview](../README.md) · [Use-case roadmap](../use-cases/README.md)

The existing gallery text is preserved here; image files are stored once in their corresponding use-case, setup, dashboard, or automation folders.

This index links to visual evidence documenting the Mini SOC lab architecture, Splunk log ingestion, SSH brute-force detection, failure-to-success authentication correlation, privilege-escalation detection, alert validation, investigation, and monitoring dashboard.

All displayed activity was generated inside an isolated and authorized lab environment.

## 1. Lab Virtual Machines

The VirtualBox environment includes the Splunk Server, Kali Linux attacker machine, and Ubuntu victim machine connected through the isolated `SOC-LAB` network.

![Lab Virtual Machines](architecture/assets/01-virtualbox-lab-environment.png)

## 2. Splunk Log Ingestion

Linux authentication logs from the monitored victim machine are successfully collected and indexed in Splunk Enterprise.

![Splunk Log Ingestion](setup/assets/01-splunk-auth-log-ingestion.png)

## 3. Raw SSH Brute-Force Events

Raw Linux authentication events show failed SSH passwords originating from the Kali Linux source address.

The logs include normal events and a compressed `message repeated` event.

![Raw SSH Brute-Force Events](../use-cases/phase-01-ssh-authentication/uc-01-ssh-bruteforce/evidence/01-raw-authentication-events.png)

## 4. Detection Query Results

The validated SPL query extracts the source IP and targeted username, calculates repeated events, and identifies six failed authentication attempts.

![SSH Detection Query Results](../use-cases/phase-01-ssh-authentication/uc-01-ssh-bruteforce/evidence/02-spl-detection-results.png)

## 5. Alert Configuration

The Splunk alert is scheduled to run every five minutes and searches the previous five-minute window.

It triggers when the detection query returns one or more results and records the alert with Medium severity.

![SSH Alert Configuration](../use-cases/phase-01-ssh-authentication/uc-01-ssh-bruteforce/evidence/03-alert-configuration.png)

## 6. Triggered Alert

The validated SSH brute-force alert appeared successfully in the Splunk Triggered Alerts page.

![Triggered SSH Alert](../use-cases/phase-01-ssh-authentication/uc-01-ssh-bruteforce/evidence/04-alert-triggered.png)

## 7. SOC Monitoring Dashboard

The SOC monitoring dashboard provides visibility into SSH detections, defensive blocks, web activity, suspicious user agents, source addresses, and recent security events.

![SOC Monitoring Dashboard](../dashboards/evidence/01-soc-monitoring-dashboard.png)

## 8. Initial Brute-Force Investigation Evidence

The investigation search confirms that the tested source IP generated failed authentication events and that no successful SSH password authentication was observed during the test window.

![SSH Investigation Evidence](../use-cases/phase-01-ssh-authentication/uc-01-ssh-bruteforce/evidence/05-investigation-results.png)

## 9. SSH Failure-to-Success Events

The raw Linux authentication events show five failed SSH password attempts against the `soc-test` account, followed by a successful password authentication from the same source IP address.

![SSH Failure-to-Success Events](../use-cases/phase-01-ssh-authentication/uc-02-ssh-failure-to-success/evidence/01-raw-failure-to-success-events.png)

## 10. SSH Failure-to-Success Detection Results

The correlation query identified five failed authentication attempts followed by a successful login from `192.168.56.30` against the `soc-test` account.

The successful login occurred approximately `6.49` seconds after the final failed attempt, and the complete sequence occurred within approximately `12.69` seconds.

![SSH Failure-to-Success Detection Results](../use-cases/phase-01-ssh-authentication/uc-02-ssh-failure-to-success/evidence/02-spl-correlation-results.png)

## 11. SSH Privilege-Escalation Detection Results

The validated correlation query identified successful SSH authentication followed by sudo command execution and the opening of a root session for the same Linux account.

Two independent privilege-escalation sequences were detected for the `soc-test` account originating from `192.168.56.30`.

The authorized command `/usr/bin/id` executed with root privileges. The measured times from SSH login to root-level execution were approximately `11.43` seconds and `5.68` seconds.

![SSH Privilege-Escalation Detection Results](../use-cases/phase-01-ssh-authentication/uc-03-ssh-privilege-escalation/evidence/01-spl-correlation-results.png)

## 12. SSH Privilege-Escalation Triggered Alert

The scheduled Splunk alert triggered successfully with Critical severity after detecting a successful SSH login followed by sudo command execution and root-session creation.

A fifteen-minute throttle was enabled and validated to suppress duplicate alerts caused by overlapping scheduled search windows.

![SSH Privilege-Escalation Triggered Alert](../use-cases/phase-01-ssh-authentication/uc-03-ssh-privilege-escalation/evidence/02-alert-triggered.png)

## Evidence Summary

| Evidence | Status |
|---|---|
| Virtual lab architecture | Documented |
| Linux log ingestion | Verified |
| Raw SSH events | Verified |
| SPL detection logic | Validated |
| Scheduled alert configuration | Validated |
| Alert triggering | Confirmed |
| SOC dashboard | Documented |
| Initial brute-force investigation | No successful authentication observed |
| Failure-to-success authentication sequence | Confirmed |
| SSH failure-to-success raw events | Verified |
| Failure-to-success correlation detection | Validated |
| SSH privilege-escalation correlation | Validated |
| Critical privilege-escalation alert | Confirmed |
| Positive and negative validation tests | Passed |
| Multiple escalation sequences | Verified |
| Duplicate-alert suppression | Verified |

## Privacy and Safety Notice

The displayed IP addresses belong to the isolated virtual lab network.

No passwords, authentication tokens, public targets, production systems, or unauthorized devices are included in this project.

## SOC Alert Automation Evidence

The following screenshots document the end-to-end SOC alert automation implemented using Splunk, n8n, and Telegram.

### 13. n8n Container Running

![n8n Container Running](../automation/n8n/evidence/01-container-running.png)

Demonstrates that the n8n Docker container is running successfully and exposing TCP port `5678`.

---

### 14. n8n Web Interface

![n8n Web Interface](../automation/n8n/evidence/02-web-interface.png)

Confirms that the n8n application is accessible and operational inside the Mini SOC lab.

---

### 15. Splunk Webhook Alert Action

![Splunk Webhook Alert Action](../automation/n8n/evidence/03-splunk-webhook-action.png)

Shows the Splunk alert configured with a Webhook alert action used to forward triggered security alerts to n8n.

Sensitive portions of the webhook endpoint should be redacted before publication.

---

### 16. n8n Webhook Reception

![n8n Webhook Reception](../automation/n8n/evidence/04-webhook-received.png)

Shows the n8n Webhook node successfully receiving alert data from Splunk.

---

### 17. n8n Workflow Execution

![n8n Workflow Execution](../automation/n8n/evidence/05-workflow-execution.png)

Shows the successful execution of the SOC automation workflow.

The implemented workflow is:

```text
Webhook
   |
   v
Remove Duplicates
   |
   v
Telegram
```

---

### 18. Duplicate Filtering

![n8n Remove Duplicates](../automation/n8n/evidence/06-deduplication-node-executed.png)

Shows the duplicate filtering stage used to reduce unnecessary repeated alert processing.

---

### 19. Telegram Node Execution

![n8n Telegram Execution](../automation/n8n/evidence/07-telegram-node-executed.png)

Shows the Telegram node executing successfully after the Splunk alert is processed by n8n.

---

### 20. Telegram SOC Alert

![Telegram SOC Alert](../automation/n8n/evidence/08-telegram-alert-delivered.png)

Shows the final SOC notification successfully delivered to the analyst through Telegram.

This screenshot confirms the complete automation chain:

```text
Splunk Detection
      |
      v
Splunk Alert
      |
      v
Webhook
      |
      v
n8n
      |
      v
Duplicate Filtering
      |
      v
Telegram
      |
      v
SOC Analyst
```

## Automation Validation Result

| Evidence | Status |
|---|---|
| n8n running | Validated |
| n8n interface accessible | Validated |
| Splunk webhook configured | Validated |
| Webhook received by n8n | Validated |
| Workflow executed | Validated |
| Duplicate filtering executed | Validated |
| Telegram node executed | Validated |
| SOC alert received in Telegram | Validated |

The evidence confirms successful end-to-end alert automation from Splunk detection to external analyst notification.

---

## Use Case 04 — Multiple Failed sudo Attempts

The following screenshots document the complete validation workflow for **Use Case 04 — Multiple Failed sudo Attempts**.

All screenshots for this use case are stored in:

```text
use-cases/phase-01-ssh-authentication/uc-04-failed-sudo/evidence/
```

### 1. Failed sudo Attempts — Event Generation

Shows the controlled generation of three incorrect sudo password attempts on the Linux victim host.

![Failed sudo Attempts](../use-cases/phase-01-ssh-authentication/uc-04-failed-sudo/evidence/01-attack-simulation.png)

### 2. Raw sudo Event in Splunk

Confirms that the generated sudo authentication event was successfully ingested from `/var/log/auth.log`.

![Raw sudo Event in Splunk](../use-cases/phase-01-ssh-authentication/uc-04-failed-sudo/evidence/02-raw-authentication-event.png)

### 3. SPL Detection Result

Shows the SPL detection extracting the affected host, user, and number of failed sudo authentication attempts.

![SPL Detection Result](../use-cases/phase-01-ssh-authentication/uc-04-failed-sudo/evidence/03-spl-field-extraction.png)

### 4. Detection Threshold Validation

Confirms that the detection threshold `failed_attempts >= 3` successfully identified the simulated activity.

![Detection Threshold Validation](../use-cases/phase-01-ssh-authentication/uc-04-failed-sudo/evidence/04-spl-threshold-results.png)

### 5. Alert Configuration

Shows the final scheduled Splunk alert configuration, including the five-minute schedule, search window, trigger condition, Medium severity, and Triggered Alerts action.

![Alert Configuration](../use-cases/phase-01-ssh-authentication/uc-04-failed-sudo/evidence/05-alert-configuration.png)

### 6. Alert Saved Successfully

Confirms that the scheduled Splunk alert was successfully saved.

![Alert Saved Successfully](../use-cases/phase-01-ssh-authentication/uc-04-failed-sudo/evidence/06-alert-saved.png)

### 7. Triggered Alert

Shows the alert successfully appearing in Splunk Triggered Alerts after the controlled sudo authentication failures.

![Triggered Alert](../use-cases/phase-01-ssh-authentication/uc-04-failed-sudo/evidence/07-alert-triggered.png)

### 8. Triggered Alert Result

Shows the triggered detection result containing the expected host, user, and failed-attempt count.

![Triggered Alert Result](../use-cases/phase-01-ssh-authentication/uc-04-failed-sudo/evidence/08-triggered-alert-results.png)

### 9. sudo Authentication Investigation

Documents the investigation of related sudo authentication failures associated with the detected user and host.

![sudo Authentication Investigation](../use-cases/phase-01-ssh-authentication/uc-04-failed-sudo/evidence/09-investigation-authentication-failures.png)

### 10. No Successful sudo Session

Shows the investigation search returning zero events for a successful root sudo session during the investigated time window.

![No Successful sudo Session](../use-cases/phase-01-ssh-authentication/uc-04-failed-sudo/evidence/10-investigation-no-root-session.png)

### Use Case 04 Evidence Summary

| Evidence | Status |
|---|---|
| Controlled sudo failure generation | Verified |
| Linux authentication log ingestion | Verified |
| SPL field extraction | Validated |
| Detection threshold | Validated |
| Scheduled alert configuration | Validated |
| Alert creation | Confirmed |
| Triggered alert | Confirmed |
| Triggered detection fields | Verified |
| sudo authentication investigation | Completed |
| Successful privileged session check | No successful session observed |

**Use Case 04 Evidence Status: COMPLETE**

## Use Case 05 — Evidence Index

[Open all 16 UC-05 evidence files](../use-cases/phase-01-ssh-authentication/uc-05-privileged-login/evidence/README.md).
