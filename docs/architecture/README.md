# Mini SOC Lab Architecture

[Project overview](../../README.md) · [Lab environment image](assets/01-virtualbox-lab-environment.png) · [Setup](../setup/README.md)

## Overview

This project is a hands-on Mini SOC lab designed to practice centralized log collection, security monitoring, detection engineering, alert triage, and incident documentation using Splunk Enterprise.

The lab generates controlled attack activity from Kali Linux against a monitored Ubuntu server. Authentication logs are then collected and analyzed in Splunk.

## Lab Components

| Component | Role |
|---|---|
| Splunk Server | Centralized log collection, analysis, alerting, and dashboarding |
| Ubuntu Server | Monitored Linux server and SSH attack target |
| Kali Linux | Controlled attack simulation machine |

## Architecture Diagram

```text
+-----------------------+
|      Kali Linux       |
|   Attacker Machine    |
|                       |
| - Hydra               |
| - SSH Login Attempts  |
+-----------+-----------+
            |
            | Controlled SSH Attacks
            v
+-----------------------+
|     Ubuntu Server     |
|   Monitored System    |
|                       |
| - SSH Service         |
| - Authentication Logs |
| - Splunk Forwarder    |
+-----------+-----------+
            |
            | Log Forwarding
            v
+-----------------------+
|     Splunk Server     |
|                       |
| - Log Collection      |
| - SPL Searches        |
| - Alerts              |
| - Dashboards          |
| - Investigation       |
+-----------------------+

