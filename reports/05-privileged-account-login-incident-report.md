# Incident Report — UC5: Successful Login to a Privileged or Sensitive Account

## Incident Summary

A successful SSH login was detected to a privileged Linux account on the monitored victim host.

The account `saeed` is classified as privileged because it is a member of the `sudo` group.

The event was generated intentionally in the controlled Mini SOC lab to validate the detection logic and alerting workflow.

## Detection Details

- Use Case: UC5 — Successful Login to a Privileged or Sensitive Account
- Severity: High
- Detection Source: Splunk
- Log Source: `/var/log/auth.log`
- Sourcetype: `linux_secure`
- Host: `victim`
- Authentication Method: Password

## Observed Event

- Timestamp: 2026-09-03 10:07:22.294
- User: `saeed`
- Account Type: Privileged Account (sudo)
- Source IP: `192.168.56.30`
- Source Port: `55576`
- Destination Host: `victim`
- Protocol: SSH
- Authentication Result: Successful

## Raw Log Evidence

```text
Accepted password for saeed from 192.168.56.30 port 55576 ssh2
```

## Investigation

The triggered alert was reviewed in Splunk.

The investigation confirmed that:

- The SSH authentication to `saeed` was successful.
- The account `saeed` is a member of the Linux `sudo` group.
- The connection originated from `192.168.56.30`.
- No failed password attempts for `saeed` were observed immediately before the detected login.
- No sudo activity associated with the detected SSH session was observed after the login.
- The SSH session was short and disconnected shortly after authentication.
- Other sudo activity visible in the surrounding logs was related to controlled lab administration and previous validation steps.

## Investigation Conclusion

Classification:

**True Positive — Authorized / Expected Activity**

The detection correctly identified a successful login to a privileged account.

The activity itself was authorized because it was intentionally generated as part of the controlled Mini SOC validation process.

## MITRE ATT&CK Mapping

### Primary Technique

- Tactic: Initial Access / Persistence / Privilege Escalation / Defense Evasion
- Technique: Valid Accounts
- Sub-technique: T1078.003 — Local Accounts

### Related Technique

- Tactic: Lateral Movement
- Technique: Remote Services
- Sub-technique: T1021.004 — SSH

## Indicators

| Indicator | Value |
|---|---|
| Source IP | `192.168.56.30` |
| User | `saeed` |
| Host | `victim` |
| Source Port | `55576` |
| Authentication Method | `password` |

## Recommended Response Actions

If this event occurred in a production environment:

1. Verify whether the privileged login was expected and authorized.
2. Confirm the identity of the user associated with the account.
3. Review activity performed during the SSH session.
4. Search for failed authentication attempts preceding the successful login.
5. Review sudo and privilege-escalation activity following authentication.
6. Investigate the source IP for additional suspicious activity.
7. Disable or restrict the account if unauthorized access is suspected.
8. Reset credentials and revoke active sessions if account compromise is confirmed.

## Detection Validation

- Raw log generated: ✅
- Raw log verified on victim: ✅
- Event ingested into Splunk: ✅
- SPL detection validated: ✅
- Privileged account lookup validated: ✅
- Positive test passed: ✅
- Negative test passed using `soc-test`: ✅
- Scheduled alert configured: ✅
- Alert triggered successfully: ✅
- Investigation completed: ✅
- MITRE ATT&CK mapped: ✅

## Final Status

**Validated**
