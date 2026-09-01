# n8n Workflow Design

## Overview

This document describes the design of the n8n workflow used to automate SOC alert notifications in the Mini SOC Monitoring Lab.

The workflow receives a triggered Splunk alert, processes the incoming event, removes duplicate executions, and sends a structured security notification to Telegram.

The implemented workflow is:

```text
Splunk Alert
     |
     v
Webhook
     |
     v
Remove Duplicates
     |
     v
Telegram
```

## Workflow Objective

The workflow was designed to:

- Receive security alerts automatically from Splunk.
- Use the Splunk alert as the workflow trigger.
- Prevent unnecessary duplicate notifications.
- Forward relevant alert information to the SOC analyst.
- Deliver the final notification through Telegram.
- Reduce manual monitoring requirements.
- Demonstrate a basic SOAR-style automation workflow.

## Workflow Nodes

The current workflow contains three main nodes:

| # | Node | Purpose |
|---|---|---|
| 1 | Webhook | Receives the triggered Splunk alert |
| 2 | Remove Duplicates | Prevents repeated processing of the same alert data |
| 3 | Telegram | Sends the final SOC notification |

## Node 1 — Webhook

The Webhook node is the entry point of the workflow.

It listens for HTTP requests sent by the Splunk Webhook alert action.

```text
Splunk
   |
   | HTTP POST
   v
Webhook Node
```

### Role

The Webhook node:

- Receives the incoming Splunk alert.
- Accepts the HTTP POST request.
- Makes the incoming alert data available to the workflow.
- Automatically starts the workflow when an alert is received.

### Method

The webhook uses:

```text
POST
```

The production endpoint follows the general structure:

```text
http://192.168.56.10:5678/webhook/<redacted-path>
```

The complete production webhook path is not published in the repository.

## Incoming Alert Data

When Splunk triggers the alert, data is sent to the Webhook node.

The received request provides alert context that can be used by the remaining workflow nodes.

Conceptually:

```text
Incoming Request
      |
      +--> Alert metadata
      |
      +--> Search information
      |
      +--> Detection result data
      |
      +--> Trigger context
```

The exact payload depends on the Splunk Webhook alert action and the search results associated with the triggered alert.

## Node 2 — Remove Duplicates

The second node is used to reduce duplicate processing.

```text
Webhook
    |
    v
Remove Duplicates
```

### Purpose

A scheduled Splunk alert may evaluate overlapping time ranges.

Without duplicate handling, the same security activity could potentially result in repeated SOC notifications.

The duplicate filtering step helps ensure that repeated copies of the same alert data are not unnecessarily forwarded to Telegram.

### Role

The Remove Duplicates node:

- Receives the event from the Webhook node.
- Evaluates incoming workflow items.
- Removes duplicate data when applicable.
- Passes only the remaining event data to the Telegram node.

### Workflow Logic

```text
Incoming Splunk Alert
        |
        v
Check for Duplicate Data
        |
     +--+--+
     |     |
Duplicate Unique
     |     |
     v     v
  Remove  Continue
              |
              v
           Telegram
```

## Why Duplicate Filtering Is Important

Duplicate notifications can create:

- Alert fatigue.
- Repeated analyst notifications.
- Unnecessary Telegram messages.
- Confusion during incident investigation.
- Reduced trust in the alerting workflow.

The duplicate filtering step improves the usability of the automation.

## Node 3 — Telegram

The Telegram node is the final stage of the current automation workflow.

```text
Remove Duplicates
        |
        v
Telegram
        |
        v
SOC Analyst
```

### Role

The Telegram node:

- Receives the processed alert data.
- Creates the final notification.
- Sends the notification through the configured Telegram Bot.
- Provides the analyst with rapid awareness of the triggered detection.

## Telegram Credentials

Telegram authentication is configured using the n8n credential system.

The bot token is stored inside n8n and is not hardcoded inside the GitHub documentation.

The following values must never be committed to the public repository:

- Telegram Bot Token
- API credentials
- Authentication secrets
- Private chat information when sensitive
- n8n credential data

## SOC Notification Structure

The Telegram notification is designed to present the security event in a readable SOC-style format.

A notification may include information such as:

```text
SOC ALERT

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

Additional fields can be included when they are available from the Splunk webhook payload.

Examples include:

- Source IP address
- Targeted username
- Failed attempt count
- Destination host
- Detection timestamp
- Alert severity
- Detection name

## Data Flow

The complete data flow inside n8n is:

```text
Webhook
   |
   | Incoming Splunk alert data
   v
Remove Duplicates
   |
   | Filtered alert data
   v
Telegram
   |
   | Formatted SOC message
   v
Analyst Notification
```

## End-to-End Workflow

The complete Mini SOC alert automation path is:

```text
Linux Authentication Event
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
Webhook Alert Action
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

## Division of Responsibilities

| Component | Responsibility |
|---|---|
| Linux Victim | Generates authentication activity |
| Splunk Universal Forwarder | Sends logs to Splunk |
| Splunk Enterprise | Stores and analyzes events |
| SPL Detection | Identifies suspicious activity |
| Scheduled Alert | Determines when the detection triggers |
| Splunk Webhook | Sends the triggered alert to n8n |
| n8n Webhook | Receives the alert |
| Remove Duplicates | Reduces repeated processing |
| Telegram | Delivers the analyst notification |

## Workflow Execution

A successful workflow execution follows this sequence:

```text
1. Security activity occurs
        |
        v
2. Splunk receives the event
        |
        v
3. SPL detection identifies the activity
        |
        v
4. Splunk alert triggers
        |
        v
5. Webhook sends the alert to n8n
        |
        v
6. n8n workflow starts
        |
        v
7. Duplicate filtering is applied
        |
        v
8. Telegram node executes
        |
        v
9. SOC notification is delivered
```

## Error Isolation

The workflow separates detection and notification responsibilities.

If Telegram delivery fails:

```text
Splunk Detection
```

can still remain operational.

If n8n is unavailable:

```text
Splunk
```

continues collecting and analyzing logs.

This design means that the automation layer extends the SIEM rather than replacing it.

## Security Considerations

The workflow documentation intentionally excludes:

- Complete active webhook paths
- Telegram Bot Token
- n8n credential data
- Passwords
- API secrets
- Session cookies

Credentials are stored locally inside the n8n credential system.

Public screenshots should also be reviewed before being committed to GitHub to ensure that no sensitive information is visible.

## Validation

The workflow was validated through end-to-end execution.

| Stage | Result |
|---|---|
| Splunk alert generated | Passed |
| Webhook request sent | Passed |
| n8n Webhook triggered | Passed |
| Alert data received | Passed |
| Duplicate filtering executed | Passed |
| Telegram node executed | Passed |
| Telegram notification received | Passed |

## Result

The workflow successfully automated the transition from a SIEM detection to an analyst notification.

Before automation:

```text
Splunk Detection
      |
      v
Splunk Alert
      |
      v
Manual Analyst Review
```

After automation:

```text
Splunk Detection
      |
      v
Splunk Alert
      |
      v
n8n Automation
      |
      v
Telegram Notification
      |
      v
SOC Analyst
```

This implementation demonstrates a practical security automation workflow and introduces basic SOAR concepts into the Mini SOC lab.
