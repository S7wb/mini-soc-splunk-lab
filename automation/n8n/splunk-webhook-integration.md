# Splunk Webhook Integration

## Overview

This document describes the integration between Splunk Enterprise and n8n inside the Mini SOC Monitoring Lab.

The purpose of the integration is to allow Splunk detections to automatically send alert information to n8n whenever a configured security alert is triggered.

n8n then receives the alert through a webhook and continues the automation workflow.

## Integration Architecture

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
Webhook Alert Action
        |
        v
HTTP POST
        |
        v
n8n Webhook
        |
        v
Automation Workflow
```

## Integration Objective

The integration was designed to:

- Automatically forward selected Splunk alerts to n8n.
- Eliminate the need to manually copy alert information between systems.
- Provide a trigger point for security automation.
- Allow additional processing of Splunk detections outside the SIEM.
- Deliver security notifications to an external analyst communication channel.

## n8n Webhook Endpoint

A Webhook node was created inside the n8n workflow to receive events from Splunk.

The webhook uses the HTTP `POST` method.

The production endpoint follows the structure:

```text
http://192.168.56.10:5678/webhook/<redacted-path>
```

The actual webhook path is intentionally excluded from the public repository.

> Sensitive webhook URLs or unique endpoint identifiers should not be published when they are being used by an active environment.

## Test URL vs Production URL

n8n provides two webhook URLs:

```text
Test URL
Production URL
```

The **Test URL** is useful while manually testing a workflow from the n8n editor.

The **Production URL** is used when the workflow is active and expected to receive events automatically.

For the Mini SOC automation, the Splunk alert action was configured to communicate with the active n8n webhook endpoint.

## Splunk Detection Alert

The first security detection connected to the automation workflow was:

**SSH Brute-Force Detection**

The detection searches Linux authentication events for repeated failed SSH authentication attempts.

When the detection meets the configured alert conditions, Splunk triggers the associated alert action.

## Webhook Alert Action

The Splunk alert was configured with a **Webhook** alert action.

The webhook destination points to the n8n Webhook node running on the Splunk Server.

The communication path is:

```text
Splunk
   |
   | HTTP POST
   v
n8n :5678
```

The n8n service listens on TCP port:

```text
5678
```

## Splunk Alert Configuration

The alert configuration includes the normal detection settings and an additional Webhook alert action.

The important integration settings are:

| Setting | Value |
|---|---|
| Detection | SSH Brute-Force Detection |
| Alert source | Splunk Enterprise |
| Alert type | Scheduled detection alert |
| Alert action | Webhook |
| Destination | n8n |
| Protocol | HTTP |
| Method | POST |
| n8n port | `5678` |
| Webhook path | Redacted from public documentation |
| Automation status | Validated |

## Alert Data Flow

When the Splunk alert triggers, Splunk creates an HTTP request containing information related to the triggered search.

The request is sent to the n8n webhook endpoint.

Conceptually, the payload contains alert context such as:

```text
Triggered Splunk Search
        |
        +--> Search / Alert Information
        |
        +--> Detection Context
        |
        +--> Result Data
        |
        +--> Trigger Metadata
```

The exact structure received by n8n depends on the data provided by the Splunk Webhook alert action.

## n8n Event Reception

The Webhook node acts as the entry point of the automation workflow.

When Splunk sends the alert:

```text
Splunk Alert
     |
     v
HTTP POST
     |
     v
n8n Webhook Node
```

n8n receives the request and makes the incoming fields available to the next nodes in the workflow.

This allows the security event to be processed automatically.

## Webhook Node Role

The Webhook node performs three main functions:

1. Listens for incoming HTTP requests.
2. Receives alert information sent by Splunk.
3. Passes the incoming data to the remaining workflow nodes.

The Webhook node does not perform the detection itself.

Detection remains the responsibility of Splunk.

The division of responsibilities is:

| Platform | Responsibility |
|---|---|
| Splunk | Log collection |
| Splunk | Detection logic |
| Splunk | Alert generation |
| Splunk | Alert triggering |
| n8n | Receive the triggered alert |
| n8n | Process the alert |
| n8n | Automation logic |
| n8n | External notification |

## Connectivity Requirements

For the integration to work, Splunk must be able to reach the n8n service.

In this lab, both services operate inside the controlled Mini SOC environment.

The required communication is:

```text
Splunk Server
     |
     v
TCP 5678
     |
     v
n8n
```

The n8n Docker container exposes:

```text
0.0.0.0:5678 -> 5678/tcp
```

This allows the webhook endpoint to receive requests through the Splunk Server's lab network interface.

## Integration Testing

The integration was tested before relying on it for automated notifications.

The validation process followed this sequence:

```text
1. Confirm n8n is running
          |
          v
2. Confirm Webhook node is available
          |
          v
3. Configure Splunk Webhook alert action
          |
          v
4. Trigger / process a Splunk alert
          |
          v
5. Verify request reaches n8n
          |
          v
6. Verify workflow execution
```

## Successful Event Reception

Successful execution inside n8n confirmed that:

- Splunk could reach the n8n service.
- TCP port `5678` was accessible.
- The webhook endpoint was configured correctly.
- Splunk successfully transmitted alert data.
- n8n successfully received the incoming request.
- The received alert could continue through the automation workflow.

## Troubleshooting

### n8n Does Not Receive the Alert

Verify that the container is running:

```bash
docker ps --filter name=n8n
```

Verify that n8n is listening on port `5678`:

```bash
docker ps
```

Expected port mapping:

```text
0.0.0.0:5678->5678/tcp
```

### Verify n8n Logs

Review the container logs:

```bash
docker logs --tail 50 n8n
```

### Verify the Webhook URL

Confirm that the URL configured in Splunk matches the webhook URL generated by the n8n Webhook node.

Verify:

- IP address
- Port
- Webhook path
- Test vs Production endpoint
- Workflow activation status

### Test vs Production Webhook

A common issue occurs when a Splunk alert is configured with an n8n **Test URL**.

Test webhooks are intended for temporary manual testing.

For automatic alert processing, the workflow should use the active production webhook endpoint.

## Security Considerations

Webhook endpoints should be treated as sensitive integration information.

The following information is intentionally excluded from this repository:

- Full active webhook URLs
- Unique webhook identifiers
- Authentication secrets
- Telegram bot tokens
- n8n credentials
- Session information
- API tokens
- Passwords

Public documentation uses sanitized examples such as:

```text
http://192.168.56.10:5678/webhook/<redacted-path>
```

instead of publishing the complete active endpoint.

## Validation

| Test | Result |
|---|---|
| n8n container running | Passed |
| Port 5678 available | Passed |
| n8n Webhook node configured | Passed |
| Splunk Webhook alert action configured | Passed |
| Splunk-to-n8n connectivity | Passed |
| HTTP request received by n8n | Passed |
| Alert data available to workflow | Passed |
| Workflow execution started automatically | Passed |

## Result

The integration successfully connected the Splunk detection layer to the n8n automation layer.

The Mini SOC workflow was extended from:

```text
Security Event
      |
      v
Splunk Detection
      |
      v
Splunk Alert
```

to:

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
```

This integration provides the foundation for automated alert processing, duplicate filtering, and SOC analyst notification.
