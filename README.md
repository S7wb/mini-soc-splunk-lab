# Mini SOC Monitoring Lab with Splunk

## Overview
This project documents a private hands-on Mini SOC lab built to practice SOC monitoring, Splunk-based detection, alerting, dashboards, log analysis, and IOC extraction.

The main use case focuses on detecting SSH brute-force attempts using Linux authentication logs.

## Lab Environment

| Component | Role |
|---|---|
| Splunk Server | SIEM and log analysis |
| Ubuntu Server | Monitored Linux server |
| Kali Linux | Attack simulation machine |
| Victim Machine | Target system for detection |

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
- Setup guide
- SPL detection query
- Alerting logic
- Dashboard documentation
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
