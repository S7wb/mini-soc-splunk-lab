# UC5 — Alert Configuration

## Alert Name

```text
Successful Login to Privileged or Sensitive Account
```

## Description

Detects successful SSH authentication to accounts classified as privileged or sensitive using the `privileged_accounts` lookup.

## Detection Query

```spl
index=* host="victim" sourcetype="linux_secure"
("Accepted password for" OR "Accepted publickey for")
| rex field=_raw "Accepted (?<auth_method>\S+) for (?<user>\S+) from (?<src_ip>\d{1,3}(?:\.\d{1,3}){3}) port (?<src_port>\d+)"
| lookup privileged_accounts.csv user OUTPUT account_type severity
| where isnotnull(account_type)
| table _time host user account_type src_ip src_port auth_method severity
| sort - _time
```

## Alert Type

```text
Scheduled
```

## Schedule

The alert runs every 5 minutes.

### Cron Expression

```text
*/5 * * * *
```

## Search Time Range

```text
Last 5 minutes
```

The search window matches the scheduled execution interval.

## Trigger Condition

```text
Number of Results > 0
```

Any successful SSH authentication event associated with an account contained in the privileged account lookup can trigger the alert.

## Trigger Mode

```text
For each result
```

Each matching privileged-account login is evaluated independently.

## Severity

```text
High
```

The Splunk alert action is configured with a default severity of `High`.

Account-specific severity is also stored in the lookup:

```csv
user,account_type,severity
saeed,Privileged Account (sudo),High
root,Sensitive Account (root),Critical
```

This allows the SPL result itself to retain account-specific severity information.

## Throttling

Throttling is enabled to reduce duplicate alerts.

### Suppression Period

```text
15 minutes
```

### Suppression Fields

```text
user,src_ip
```

This means repeated detections involving the same privileged user and source IP are suppressed during the configured throttle period.

A different source IP or different privileged account can still produce an independent alert.

## Trigger Action

```text
Add to Triggered Alerts
```

This action records the detection in the Splunk Triggered Alerts interface for analyst review and investigation.

## Lookup Dependency

The alert depends on:

```text
lookups/privileged_accounts.csv
```

The lookup contains the accounts that are considered privileged or sensitive.

Current validated entries:

| User | Account Type | Severity |
|---|---|---|
| `saeed` | Privileged Account (sudo) | High |
| `root` | Sensitive Account (root) | Critical |

The `saeed` account was manually verified as a member of the Linux `sudo` group.

## Positive Validation

A successful SSH login was performed using:

```text
saeed@192.168.56.20
```

Source:

```text
192.168.56.30
```

The account matched the privileged account lookup and generated a detection result.

Result:

```text
PASS
```

## Negative Validation

A successful SSH login was performed using the non-privileged account:

```text
soc-test
```

The authentication event was successfully ingested into Splunk.

However, `soc-test` was not present in `privileged_accounts.csv` and therefore did not appear in the UC5 detection results.

Result:

```text
PASS
```

## Trigger Validation

A new successful SSH login to the `saeed` account generated the following alert result:

| Field | Value |
|---|---|
| User | `saeed` |
| Host | `victim` |
| Account Type | Privileged Account (sudo) |
| Source IP | `192.168.56.30` |
| Source Port | `55576` |
| Authentication Method | `password` |
| Severity | `High` |

The scheduled alert successfully appeared in:

```text
Activity → Triggered Alerts
```

Trigger validation result:

```text
PASS
```

## Final Configuration

| Setting | Value |
|---|---|
| Alert Type | Scheduled |
| Schedule | Every 5 minutes |
| Cron | `*/5 * * * *` |
| Search Window | Last 5 minutes |
| Trigger Condition | Number of Results > 0 |
| Trigger Mode | For each result |
| Throttle | Enabled |
| Suppression Period | 15 minutes |
| Suppression Fields | `user,src_ip` |
| Trigger Action | Add to Triggered Alerts |
| Default Alert Severity | High |

## Validation Status

- Detection query validated: ✅
- Lookup dependency validated: ✅
- Positive test passed: ✅
- Negative test passed: ✅
- Scheduled alert created: ✅
- Throttling configured: ✅
- Alert triggered successfully: ✅
- Triggered alert results reviewed: ✅

## Final Status

**Validated**
