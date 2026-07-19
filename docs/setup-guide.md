# Mini SOC Lab Setup Guide

## Overview

This guide documents the setup used to build the Mini SOC lab with Splunk Enterprise.

The environment consists of three virtual machines:

| System | Purpose |
|---|---|
| Splunk Server | Centralized log collection, searching, alerting, and dashboards |
| Victim Machine | Linux system monitored by Splunk and targeted during authorized tests |
| Kali Linux | Controlled attack simulation machine |

## Lab Requirements

- VirtualBox or another virtualization platform
- Ubuntu Server for Splunk Enterprise
- Ubuntu or another supported Linux distribution for the victim machine
- Kali Linux for controlled testing
- Splunk Enterprise
- Splunk Universal Forwarder
- OpenSSH Server
- Hydra
- An isolated virtual network

## Network Configuration

All virtual machines must be able to communicate with each other inside an isolated lab network.

Before continuing, identify the current IP address of each machine:

```bash
hostname -I
```

IP addresses assigned by DHCP may change after restarting a virtual machine. Always confirm the current address before running tests.

Example lab roles:

| System | Example Hostname |
|---|---|
| Splunk Server | `splunk-server` |
| Victim Machine | `victim` |
| Kali Linux | `kali` |

## 1. Splunk Server Setup

Install Splunk Enterprise on the Ubuntu Splunk Server and start the service.

After installation, access the Splunk web interface through:

```text
http://<SPLUNK_SERVER_IP>:8000
```

Replace `<SPLUNK_SERVER_IP>` with the current IP address of the Splunk Server.

### Enable Log Receiving

In Splunk Enterprise:

1. Open **Settings**.
2. Select **Forwarding and receiving**.
3. Open **Configure receiving**.
4. Select **New Receiving Port**.
5. Enter:

```text
9997
```

6. Save the receiving port.

The Splunk Server should now accept data from the Universal Forwarder.

## 2. Victim Machine Setup

### Install and Enable SSH

On the victim machine:

```bash
sudo apt update
sudo apt install openssh-server -y
sudo systemctl enable --now ssh
```

Verify that SSH is running:

```bash
sudo systemctl status ssh --no-pager
```

The expected status is:

```text
Active: active (running)
```

Confirm the victim machine IP address:

```bash
hostname -I
```

### Verify Authentication Logs

Confirm that the authentication log exists:

```bash
sudo ls -l /var/log/auth.log
```

Monitor the file during testing:

```bash
sudo tail -f /var/log/auth.log
```

## 3. Splunk Universal Forwarder Setup

Install Splunk Universal Forwarder on the victim machine.

The default installation directory used in this lab is:

```text
/opt/splunkforwarder
```

Start the forwarder and accept the license:

```bash
sudo /opt/splunkforwarder/bin/splunk start --accept-license
```

Configure the forwarder to send data to the Splunk Server:

```bash
sudo /opt/splunkforwarder/bin/splunk add forward-server <SPLUNK_SERVER_IP>:9997
```

Replace `<SPLUNK_SERVER_IP>` with the actual address of the Splunk Server.

Add the Linux authentication log as a monitored source:

```bash
sudo /opt/splunkforwarder/bin/splunk add monitor /var/log/auth.log -index main
```

Restart the forwarder:

```bash
sudo /opt/splunkforwarder/bin/splunk restart
```

Enable automatic startup:

```bash
sudo /opt/splunkforwarder/bin/splunk enable boot-start
```

### Verify Forwarder Connectivity

Check the configured forwarding destination:

```bash
sudo /opt/splunkforwarder/bin/splunk list forward-server
```

The Splunk Server should appear as an active forwarding destination.

## 4. Verify Log Ingestion in Splunk

Open **Search & Reporting** in Splunk and run:

```spl
index=main source="/var/log/auth.log"
| table _time host source _raw
| sort - _time
```

Expected results should include:

- Authentication events from the victim machine
- `host` showing the monitored system
- `source` showing `/var/log/auth.log`
- Raw Linux authentication events

If no events appear, review the troubleshooting section below.

## 5. Kali Linux Test Preparation

Hydra is used only to generate controlled failed SSH login attempts inside the isolated lab.

Confirm that Hydra is installed:

```bash
hydra -h
```

Create a small password list containing intentionally incorrect passwords:

```bash
printf "1234\n12345\nadmin\npassword\ntest\nqwerty\n" > ssh-test.txt
```

Confirm the current victim machine IP before running the test:

```bash
ping -c 3 <VICTIM_IP>
```

## 6. Generate Controlled SSH Activity

Run the following command from Kali Linux:

```bash
hydra -l <TEST_USERNAME> -P ssh-test.txt -t 1 -V ssh://<VICTIM_IP>
```

Replace:

- `<TEST_USERNAME>` with the authorized test account
- `<VICTIM_IP>` with the current victim machine IP address

Example:

```bash
hydra -l saeed -P ssh-test.txt -t 1 -V ssh://192.168.56.20
```

Only incorrect test passwords should be included in the password list.

## 7. Validate the Detection

In Splunk, set the search time range to:

```text
Last 5 minutes
```

Run the validated detection stored in:

```text
detections/ssh-bruteforce-detection.spl
```

The expected output includes:

| Field | Description |
|---|---|
| `host` | Victim system receiving the attempts |
| `src_ip` | Kali Linux source IP address |
| `targeted_users` | Account targeted by Hydra |
| `failed_attempts` | Number of failed login attempts |
| `first_seen` | First observed attempt |
| `last_seen` | Latest observed attempt |
| `duration_seconds` | Duration of the activity |

The detection triggers when five or more failed SSH login attempts originate from the same source IP during the selected search window.

## 8. Recommended Alert Configuration

After validating the query, save it as a Splunk alert.

Suggested configuration:

| Setting | Value |
|---|---|
| Alert type | Scheduled |
| Schedule | Every 5 minutes |
| Search time range | Last 5 minutes |
| Trigger condition | Number of results is greater than 0 |
| Severity | Medium |

The alert severity should be increased if repeated failures are followed by a successful SSH login from the same source IP.

## Troubleshooting

### No SSH Events Appear in Splunk

Confirm the current victim IP:

```bash
hostname -I
```

Confirm that SSH is active:

```bash
sudo systemctl status ssh --no-pager
```

Check recent SSH activity:

```bash
sudo journalctl -u ssh --since "20 minutes ago" --no-pager
```

Check whether `/var/log/auth.log` is updating:

```bash
sudo tail -n 50 /var/log/auth.log
```

Check the Universal Forwarder status:

```bash
sudo /opt/splunkforwarder/bin/splunk status
```

Check the forwarding destination:

```bash
sudo /opt/splunkforwarder/bin/splunk list forward-server
```

### Events Appear but the Detection Returns No Results

Verify that:

- The search time range includes the test activity
- The events contain `Failed password`
- The process name contains `sshd`
- The correct index is being searched
- The log source matches `/var/log/auth.log`
- At least five failed attempts occurred

### IP Address Changed

Virtual machine IP addresses may change after restarting the lab.

Always run:

```bash
hostname -I
```

before testing and update the Hydra destination address accordingly.

## Environment-Specific Values

The following values may differ in another environment:

| Setting | Lab Value |
|---|---|
| Splunk index | `main` |
| Authentication log source | `/var/log/auth.log` |
| Receiving port | `9997` |
| Splunk web port | `8000` |
| SSH port | `22` |
| Detection threshold | `5` failed attempts |
| Search window | Last 5 minutes |

## Safety Notice

All attack simulations must be performed only against systems owned by the tester or systems where explicit authorization has been granted.

This setup is intended for an isolated educational lab and must not be used against public, production, or unauthorized systems.
