# Telegram Integration

## Overview

This document describes the Telegram integration used in the Mini SOC Monitoring Lab.

Telegram is used as the analyst notification channel for the n8n security automation workflow.

When a Splunk detection triggers, the alert is sent to n8n through a webhook. After the event is processed, n8n sends a structured SOC notification to Telegram.

## Integration Architecture

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
Remove Duplicates
      |
      v
Telegram Bot
      |
      v
SOC Analyst
```

## Objective

The Telegram integration was implemented to:

- Deliver SOC alerts outside the Splunk interface.
- Notify the analyst when a detection is triggered.
- Reduce the need for continuous manual monitoring.
- Provide a readable summary of the detected event.
- Demonstrate automated alert delivery as part of a SOAR-style workflow.

## Telegram Bot

A dedicated Telegram Bot was created for the Mini SOC lab.

The bot is used only as the delivery mechanism for automated SOC notifications.

The Telegram Bot Token is treated as a secret and is not included in this repository.

The token is stored inside the n8n credential system.

## n8n Telegram Credentials

The Telegram node uses credentials configured directly inside n8n.

The credential configuration contains the Telegram Bot Token required to communicate with the Telegram Bot API.

Sensitive credential values are not hardcoded inside the workflow documentation.

The following information must not be published:

- Telegram Bot Token
- Authentication secrets
- API keys
- Private credential values
- Session information

## Telegram Node

The Telegram node is the final node in the current automation workflow.

```text
Webhook
   |
   v
Remove Duplicates
   |
   v
Telegram
```

The node receives the processed alert data and sends a message to the configured Telegram destination.

## Telegram Destination

The Telegram node sends the notification to the configured analyst chat.

The destination is defined using the Telegram Chat ID.

The public documentation may reference the use of a Chat ID, but sensitive or personal identifiers should not be exposed unnecessarily.

Example:

```text
Chat ID: <redacted>
```

## Notification Design

The Telegram message is structured to make the alert easy to read.

The notification presents important SOC information in a concise format.

Example structure:

```text
🚨 SOC ALERT

Detection:
SSH Brute Force Detection

Severity:
Medium

Source:
Splunk

Status:
Triggered

Action:
Review the event in Splunk for additional investigation.
```

## Security Event Context

When the required fields are available from the Splunk alert payload, the notification can also include:

- Detection name
- Severity
- Source IP address
- Targeted account
- Destination host
- Failed authentication count
- Timestamp
- Alert status

This gives the analyst useful context before opening Splunk for deeper investigation.

## Example Detailed Alert

A more detailed message can follow this structure:

```text
🚨 SOC ALERT

Detection: SSH Brute Force Detection
Severity: Medium

Source IP: <source-ip>
Target User: <username>
Destination Host: <host>
Failed Attempts: <count>

Source: Splunk
Status: Triggered

Action:
Review the alert in Splunk and investigate the source activity.
```

Values shown in public documentation should be sanitized when necessary.

## Alert Delivery Flow

The notification process follows this sequence:

```text
1. Splunk detection triggers
        |
        v
2. Splunk sends webhook request
        |
        v
3. n8n receives the alert
        |
        v
4. Duplicate filtering is applied
        |
        v
5. Telegram message is generated
        |
        v
6. Telegram Bot sends notification
        |
        v
7. SOC analyst receives the alert
```

## Role of Telegram

Telegram is used only as a notification channel.

It does not perform:

- Log collection
- Detection
- Correlation
- Event storage
- Incident investigation

These responsibilities remain with Splunk and the analyst.

The responsibility model is:

| Component | Responsibility |
|---|---|
| Splunk | Log collection and detection |
| Splunk Alert | Determines when the detection triggers |
| Webhook | Transfers the alert |
| n8n | Processes and automates the event |
| Telegram Bot | Delivers the notification |
| SOC Analyst | Investigates and responds |

## Why Telegram Was Used

Telegram provides a simple notification channel for the lab and allows security alerts to be delivered quickly to the analyst.

For a production SOC environment, similar automation concepts could be integrated with platforms such as:

- Microsoft Teams
- Slack
- Email
- Ticketing systems
- Incident response platforms
- Enterprise SOAR solutions

Telegram is used in this lab to demonstrate the automation concept in a controlled environment.

## Testing

The Telegram integration was tested as part of the complete workflow.

The validation sequence was:

```text
Splunk Alert
     |
     v
n8n Webhook
     |
     v
Remove Duplicates
     |
     v
Telegram Node
     |
     v
Telegram Message Received
```

Successful message delivery confirmed that:

- The Telegram credentials were valid.
- The Telegram Bot was operational.
- The configured destination was reachable.
- The n8n Telegram node executed successfully.
- Alert information could be delivered to the analyst.

## Validation

| Test | Result |
|---|---|
| Telegram Bot created | Passed |
| Bot credentials configured in n8n | Passed |
| Telegram node configured | Passed |
| Destination chat configured | Passed |
| n8n workflow reached Telegram node | Passed |
| SOC alert message sent | Passed |
| SOC notification received | Passed |
| End-to-end alert delivery | Passed |

## Security Considerations

Telegram credentials must be protected.

The following values are intentionally excluded from GitHub:

- Telegram Bot Token
- Credential secrets
- Private authentication information
- Sensitive Chat IDs
- Session cookies
- API keys

Public screenshots must be reviewed before upload to make sure no sensitive credential information is visible.

If a token is accidentally exposed publicly, it should be considered compromised and replaced immediately.

## Result

The Telegram integration successfully completed the automated SOC alert delivery chain.

The final workflow is:

```text
Security Event
      |
      v
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
SOC Analyst Notification
```

This demonstrates how a SIEM detection can be extended into an automated analyst notification workflow using n8n.
