# Use-Case Roadmap

[Project overview](../README.md)

UC-01 to UC-05 contain the existing lab documentation, SPL, reports, and available screenshots. This repository restructuring did not rerun the lab or reassess all prior validation claims. UC-06 to UC-48 are planned templates with no detection SPL or invented evidence.

The severity column describes the roadmap target. UC-04's existing documentation uses Medium while its roadmap target is High; both values are retained and require a separate alignment decision.

## SSH Authentication

[Open phase index](phase-01-ssh-authentication/README.md)

| UC | Use case | Roadmap severity | Material status |
|---|---|---|---|
| UC-01 | [SSH Brute-Force Detection](phase-01-ssh-authentication/uc-01-ssh-bruteforce/README.md) | Medium | Existing documentation — validation not repeated |
| UC-02 | [SSH Brute Force Followed by Successful Login](phase-01-ssh-authentication/uc-02-ssh-failure-to-success/README.md) | High | Existing documentation — validation not repeated |
| UC-03 | [Successful SSH Login Followed by Privilege Escalation](phase-01-ssh-authentication/uc-03-ssh-privilege-escalation/README.md) | Critical | Existing documentation — validation not repeated |
| UC-04 | [Multiple Failed sudo Attempts](phase-01-ssh-authentication/uc-04-failed-sudo/README.md) | High | Existing documentation — validation not repeated |
| UC-05 | [Successful Login to a Privileged or Sensitive Account](phase-01-ssh-authentication/uc-05-privileged-login/README.md) | High / Critical | Existing documentation — validation not repeated |

## Linux Post-Compromise

[Open phase index](phase-02-linux-post-compromise/README.md)

| UC | Use case | Roadmap severity | Material status |
|---|---|---|---|
| UC-06 | [New Local User Created After SSH Login](phase-02-linux-post-compromise/uc-06-new-local-user-after-ssh/README.md) | High | Planned — Not Yet Implemented or Validated |
| UC-07 | [User Added to sudo Group](phase-02-linux-post-compromise/uc-07-user-added-to-sudo-group/README.md) | Critical | Planned — Not Yet Implemented or Validated |
| UC-08 | [Suspicious Command Download](phase-02-linux-post-compromise/uc-08-suspicious-command-download/README.md) | High | Planned — Not Yet Implemented or Validated |
| UC-09 | [Suspicious Script or Binary Execution](phase-02-linux-post-compromise/uc-09-suspicious-script-or-binary-execution/README.md) | High | Planned — Not Yet Implemented or Validated |
| UC-10 | [Cron Job Persistence](phase-02-linux-post-compromise/uc-10-cron-job-persistence/README.md) | High | Planned — Not Yet Implemented or Validated |
| UC-11 | [Systemd Service Persistence](phase-02-linux-post-compromise/uc-11-systemd-service-persistence/README.md) | Critical | Planned — Not Yet Implemented or Validated |
| UC-12 | [SSH Key Persistence](phase-02-linux-post-compromise/uc-12-ssh-key-persistence/README.md) | Critical | Planned — Not Yet Implemented or Validated |
| UC-13 | [Sensitive File Access](phase-02-linux-post-compromise/uc-13-sensitive-file-access/README.md) | High | Planned — Not Yet Implemented or Validated |
| UC-14 | [Authentication Log Tampering](phase-02-linux-post-compromise/uc-14-authentication-log-tampering/README.md) | Critical | Planned — Not Yet Implemented or Validated |
| UC-15 | [Shell History Tampering](phase-02-linux-post-compromise/uc-15-shell-history-tampering/README.md) | High | Planned — Not Yet Implemented or Validated |

## Defensive Response and Control

[Open phase index](phase-03-defensive-response/README.md)

| UC | Use case | Roadmap severity | Material status |
|---|---|---|---|
| UC-16 | [Fail2Ban Block Detection](phase-03-defensive-response/uc-16-fail2ban-block-detection/README.md) | Medium | Planned — Not Yet Implemented or Validated |
| UC-17 | [Repeated Attacks After Unban](phase-03-defensive-response/uc-17-repeated-attacks-after-unban/README.md) | High | Planned — Not Yet Implemented or Validated |
| UC-18 | [Multi-Host SSH Attack](phase-03-defensive-response/uc-18-multi-host-ssh-attack/README.md) | High | Planned — Not Yet Implemented or Validated |
| UC-19 | [Distributed SSH Brute Force](phase-03-defensive-response/uc-19-distributed-ssh-bruteforce/README.md) | High | Planned — Not Yet Implemented or Validated |
| UC-20 | [Low-and-Slow Password Guessing](phase-03-defensive-response/uc-20-low-and-slow-password-guessing/README.md) | Medium / High | Planned — Not Yet Implemented or Validated |

## Web Monitoring

[Open phase index](phase-04-web-monitoring/README.md)

| UC | Use case | Roadmap severity | Material status |
|---|---|---|---|
| UC-21 | [Excessive HTTP 404 Errors](phase-04-web-monitoring/uc-21-excessive-http-404-errors/README.md) | Medium | Planned — Not Yet Implemented or Validated |
| UC-22 | [Directory and File Enumeration](phase-04-web-monitoring/uc-22-directory-and-file-enumeration/README.md) | Medium | Planned — Not Yet Implemented or Validated |
| UC-23 | [Suspicious User-Agent Detection](phase-04-web-monitoring/uc-23-suspicious-user-agent/README.md) | Medium | Planned — Not Yet Implemented or Validated |
| UC-24 | [Path Traversal Attempt](phase-04-web-monitoring/uc-24-path-traversal-attempt/README.md) | High | Planned — Not Yet Implemented or Validated |
| UC-25 | [SQL Injection Indicators](phase-04-web-monitoring/uc-25-sql-injection-indicators/README.md) | High | Planned — Not Yet Implemented or Validated |
| UC-26 | [Cross-Site Scripting Indicators](phase-04-web-monitoring/uc-26-cross-site-scripting-indicators/README.md) | High | Planned — Not Yet Implemented or Validated |
| UC-27 | [Web Login Brute Force](phase-04-web-monitoring/uc-27-web-login-bruteforce/README.md) | High | Planned — Not Yet Implemented or Validated |
| UC-28 | [Successful Login After Web Brute Force](phase-04-web-monitoring/uc-28-successful-login-after-web-bruteforce/README.md) | Critical | Planned — Not Yet Implemented or Validated |
| UC-29 | [Webshell Access Indicators](phase-04-web-monitoring/uc-29-webshell-access-indicators/README.md) | Critical | Planned — Not Yet Implemented or Validated |

## Network and Suspicious Communications

[Open phase index](phase-05-network/README.md)

| UC | Use case | Roadmap severity | Material status |
|---|---|---|---|
| UC-30 | [Port Scan Detection](phase-05-network/uc-30-port-scan-detection/README.md) | Medium | Planned — Not Yet Implemented or Validated |
| UC-31 | [Reverse Shell Detection](phase-05-network/uc-31-reverse-shell-detection/README.md) | Critical | Planned — Not Yet Implemented or Validated |
| UC-32 | [Outbound Connection to Unusual Port](phase-05-network/uc-32-outbound-connection-unusual-port/README.md) | High | Planned — Not Yet Implemented or Validated |
| UC-33 | [C2 Beaconing](phase-05-network/uc-33-c2-beaconing/README.md) | Critical | Planned — Not Yet Implemented or Validated |
| UC-34 | [Data Exfiltration Indicators](phase-05-network/uc-34-data-exfiltration-indicators/README.md) | Critical | Planned — Not Yet Implemented or Validated |
| UC-35 | [DNS Tunneling Indicators](phase-05-network/uc-35-dns-tunneling-indicators/README.md) | High | Planned — Not Yet Implemented or Validated |

## Windows and Sysmon

[Open phase index](phase-06-windows-sysmon/README.md)

| UC | Use case | Roadmap severity | Material status |
|---|---|---|---|
| UC-36 | [Windows Failed Logon Brute Force](phase-06-windows-sysmon/uc-36-windows-failed-logon-bruteforce/README.md) | Medium | Planned — Not Yet Implemented or Validated |
| UC-37 | [Failed Logons Followed by Success](phase-06-windows-sysmon/uc-37-failed-logons-followed-by-success/README.md) | High | Planned — Not Yet Implemented or Validated |
| UC-38 | [Suspicious PowerShell Execution](phase-06-windows-sysmon/uc-38-suspicious-powershell-execution/README.md) | High | Planned — Not Yet Implemented or Validated |
| UC-39 | [Encoded PowerShell Command](phase-06-windows-sysmon/uc-39-encoded-powershell-command/README.md) | Critical | Planned — Not Yet Implemented or Validated |
| UC-40 | [New Local User Creation](phase-06-windows-sysmon/uc-40-new-local-user-creation/README.md) | High | Planned — Not Yet Implemented or Validated |
| UC-41 | [User Added to Administrators Group](phase-06-windows-sysmon/uc-41-user-added-to-administrators/README.md) | Critical | Planned — Not Yet Implemented or Validated |
| UC-42 | [Scheduled Task Persistence](phase-06-windows-sysmon/uc-42-scheduled-task-persistence/README.md) | High | Planned — Not Yet Implemented or Validated |
| UC-43 | [New Service Installation](phase-06-windows-sysmon/uc-43-new-service-installation/README.md) | Critical | Planned — Not Yet Implemented or Validated |
| UC-44 | [Registry Run-Key Persistence](phase-06-windows-sysmon/uc-44-registry-run-key-persistence/README.md) | High | Planned — Not Yet Implemented or Validated |
| UC-45 | [Windows Defender Disabled](phase-06-windows-sysmon/uc-45-windows-defender-disabled/README.md) | Critical | Planned — Not Yet Implemented or Validated |
| UC-46 | [Suspicious Process and Network Correlation](phase-06-windows-sysmon/uc-46-suspicious-process-network-correlation/README.md) | High | Planned — Not Yet Implemented or Validated |
| UC-47 | [Credential Dumping Indicators](phase-06-windows-sysmon/uc-47-credential-dumping-indicators/README.md) | Critical | Planned — Not Yet Implemented or Validated |
| UC-48 | [Lateral Movement Indicators](phase-06-windows-sysmon/uc-48-lateral-movement-indicators/README.md) | Critical | Planned — Not Yet Implemented or Validated |

## Completion Rule

- [ ] Generate the scenario in the authorized lab.
- [ ] Verify source events and ingestion into Splunk.
- [ ] Develop and test SPL with positive and negative scenarios.
- [ ] Configure the alert and retain trigger evidence.
- [ ] Verify the MITRE ATT&CK mapping and its limits.
- [ ] Investigate and complete the incident report.
- [ ] Add screenshots, captions, and observed results.
- [ ] Validate linked automation when applicable.
