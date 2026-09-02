# Alert Configuration — Multiple Failed sudo Attempts

## Overview

This document describes the Splunk alert configuration used for **Use Case 04 — Multiple Failed sudo Attempts**.

The alert monitors Linux authentication logs for three or more incorrect `sudo` password attempts and generates a scheduled alert when the detection returns one or more results.

---

## Detection Search

The alert uses the following SPL:

```spl
index=* source="/var/log/auth.log" "incorrect password attempts"
| rex field=_raw "sudo:\s+(?<user>\S+)\s+:\s+(?<failed_attempts>\d+)\s+incorrect password attempts"
| where failed_attempts >= 3
| table _time host user failed_attempts
```

---

## Alert Settings

| Setting | Value |
|---|---|
| Alert Name | `Multiple Failed sudo Attempts` |
| Alert Type | Scheduled |
| Time Range | Last 5 minutes |
| Cron Expression | `*/5 * * * *` |
| Schedule | Every 5 minutes |
| Trigger Condition | Number of Results is greater than `0` |
| Trigger Mode | Once |
| Severity | Medium |
| Trigger Action | Add to Triggered Alerts |

---

## Detection Threshold

The SPL applies the following threshold:

```spl
| where failed_attempts >= 3
```

Therefore, only events reporting three or more incorrect sudo password attempts are returned by the detection.

The Splunk alert then triggers when:

```text
Number of Results > 0
```

---

## Scheduling

The alert uses the following cron expression:

```text
*/5 * * * *
```

This executes the detection every five minutes.

The search window is configured as:

```text
Last 5 minutes
```

This allows each scheduled execution to inspect recent authentication activity for matching sudo failures.

---

## Trigger Action

The following trigger action is enabled:

```text
Add to Triggered Alerts
```

This allows successful detections to appear in Splunk's **Triggered Alerts** interface for analyst review and investigation.

---

## Alert Validation

After the alert was created, another controlled test was performed on the Linux victim host.

The sudo credential cache was invalidated:

```bash
sudo -k
```

The following command was executed:

```bash
sudo whoami
```

Three incorrect passwords were entered.

The generated event satisfied:

```text
failed_attempts >= 3
```

During the next scheduled execution, the alert successfully appeared in **Triggered Alerts**.

### Triggered Result

The alert result contained:

| Field | Value |
|---|---|
| Host | `victim` |
| User | `saeed` |
| Failed Attempts | `3` |

This confirmed that the complete alert workflow operated successfully.

---

## Validation Result

| Validation | Status |
|---|---|
| SPL returns expected sudo event | PASS |
| Threshold `failed_attempts >= 3` works | PASS |
| Scheduled search executes | PASS |
| Alert triggers on matching event | PASS |
| Alert appears in Triggered Alerts | PASS |
| Triggered result contains expected fields | PASS |

**Overall Alert Validation: PASS**

---

## Analyst Notes

The alert identifies repeated failed sudo authentication attempts but does not by itself prove that privilege escalation was successful.

After the alert triggers, the analyst should review surrounding authentication activity and determine whether a successful privileged session followed the failures.

During this lab validation, a search for:

```spl
index=* source="/var/log/auth.log" host="victim" "sudo" "session opened for user root"
```

returned:

```text
0 events
```

No evidence of successful privilege escalation was identified during the investigated time window.
