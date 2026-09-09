# UC-06 — New Local User Created After SSH Login — Incident Report

[Use case](README.md)

**Status:** Validated

## Scope and Scenario

This incident report documents the authorized execution and investigation of UC-06 in the isolated Mini SOC lab environment.

The scenario simulated a successful SSH login to the Linux victim host followed by creation of a new local user account.

Observed systems and accounts:

- Victim host: `victim`
- Victim IP: `192.168.56.20`
- SSH source IP: `192.168.56.30`
- SSH account: `soc-test`
- Created account: `soc-alerttest`
- Log source: `/var/log/auth.log`
- Splunk sourcetype: `linux_secure`

The test was performed in a controlled lab environment for defensive detection validation.

## Timeline and Timezone

Timezone: `UTC+03:00`

| Time | Event |
|---|---|
| 2026-09-07 10:24 approximately | Successful SSH login to `soc-test` from `192.168.56.30` |
| 2026-09-07 10:24 approximately | `soc-test` executed `/usr/sbin/useradd soc-alerttest` with `sudo` |
| 2026-09-07 10:24 approximately | Linux logged successful creation of the `soc-alerttest` local account |
| 2026-09-07 10:25:01 | Scheduled Splunk alert triggered |
| Detection result | Time between SSH login and account creation: `38.55 seconds` |

The exact source timestamps are preserved in the Splunk evidence screenshots.

## Evidence and Analysis

Supporting evidence: [UC-06 Evidence Index](evidence/README.md)

### Successful SSH Login

Splunk identified a successful SSH login associated with:

- User: `soc-test`
- Source IP: `192.168.56.30`
- Host: `victim`

This login became the preceding authentication event used by the UC-06 correlation logic.

### Local Account Creation

The account creation was confirmed in `/var/log/auth.log`.

Observed activity included:

- `sudo` execution by `soc-test`
- Command: `/usr/sbin/useradd soc-alerttest`
- Execution context: `USER=root`
- Creation of a new local group
- Creation of the new user `soc-alerttest`

The successful `useradd: new user:` event confirmed that the account was actually created rather than only attempted.

### Detection Correlation

The Splunk detection correlated the successful SSH login with the subsequent account creation.

Observed detection fields:

| Field | Value |
|---|---|
| Host | `victim` |
| Login user | `soc-test` |
| Login source IP | `192.168.56.30` |
| New local user | `soc-alerttest` |
| Time to creation | `38.55 seconds` |

The detection logic requires the account creation event to occur within `600 seconds` after the preceding successful SSH login.

### Alert Validation

The scheduled alert:

`New Local User Created After SSH Login`

successfully triggered in Splunk.

Observed alert properties:

- Severity: `High`
- Schedule: every 5 minutes
- Search time range: Last 10 minutes
- Trigger condition: Number of Results `> 0`
- Trigger mode: Trigger Once
- Alert action: Add to Triggered Alerts

The alert appeared in Splunk Triggered Alerts at:

`2026-09-07 10:25:01 UTC+03:00`

### Negative Test

A second local account, `soc-localtest`, was created directly from the victim system without a qualifying SSH login in the correlation search window.

The account creation event was successfully ingested into Splunk.

However, the UC-06 correlation detection returned:

`0 events`

This validated that the detection did not trigger solely because a local account creation event existed.

### Post-Creation Activity

A follow-up search was performed for successful authentication or an opened session using the newly created account `soc-alerttest`.

No matching events were found.

Therefore, no evidence was observed that `soc-alerttest` was used for a successful login after creation during the investigation window.

## MITRE ATT&CK Mapping

| Field | Mapping |
|---|---|
| Tactic | Persistence |
| Tactic ID | `TA0003` |
| Technique | Create Account |
| Technique ID | `T1136` |
| Sub-technique | Local Account |
| Sub-technique ID | `T1136.001` |

The observed behavior is consistent with creation of a local account that could be used to maintain access to a compromised Linux system.

## Findings, Response, and Limitations

### Findings

The investigation confirmed:

- A successful SSH login occurred using `soc-test`.
- The SSH source IP was `192.168.56.30`.
- The same test sequence was followed by privileged execution of `useradd`.
- The account `soc-alerttest` was successfully created.
- The creation occurred `38.55 seconds` after the correlated SSH login.
- The scheduled Splunk alert triggered successfully.
- The negative test did not produce a correlated detection.
- No successful login using `soc-alerttest` was observed after account creation.

### Analyst Assessment

In a production environment, creation of a new local user shortly after remote access should be treated as suspicious unless the activity is verified as authorized administrative work.

The activity may indicate an attacker attempting to establish persistence after obtaining remote access.

### Recommended Response

For an unexpected production event, the analyst should:

1. Validate whether the new account creation was authorized.
2. Identify the user and source system responsible for the preceding SSH login.
3. Review the privileges, groups, shell, and configuration of the new account.
4. Search for subsequent authentication or command activity performed by the new account.
5. Review related privilege escalation activity.
6. Disable or remove the account if confirmed unauthorized.
7. Investigate the originating host and account for additional compromise indicators.
8. Preserve relevant authentication and system logs for further investigation.

### Limitations

- This use case was executed in an isolated lab and does not represent a real compromise.
- The detection correlates account creation with the most recent successful SSH login identified on the host within the configured time window.
- The current correlation does not prove that the SSH user directly caused every detected account creation event.
- Shared hosts with multiple simultaneous SSH sessions may require stronger session-level or process-level correlation.
- The detection currently relies on Linux authentication log content and the observed `useradd` logging format.
- No evidence was observed that the created account was subsequently used for authentication during this test.

## Incident Status

**Closed — Authorized Lab Validation**

## Validation Result

**PASS**
