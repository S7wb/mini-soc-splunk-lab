# Lessons Learned

## Overview

This document summarizes the technical and operational lessons learned while building the Mini SOC lab with Splunk Enterprise.

The project provided hands-on experience in log collection, detection development, alert investigation, and incident documentation.

## 1. Log Collection Must Be Verified First

A detection cannot work correctly unless the required logs are being collected and indexed.

Before writing an SPL query, it is important to verify:

- The monitored log file exists
- The Splunk Universal Forwarder is running
- The forwarder is connected to the Splunk Server
- Events are reaching the correct index
- The expected fields and raw events are available

This helped prevent troubleshooting detection logic when the actual issue was missing or incomplete log ingestion.

## 2. Raw Logs Should Be Reviewed Before Writing SPL

Reviewing the raw authentication events made it easier to understand the structure of failed and successful SSH login records.

Important fields and values included:

- Source IP address
- Username
- Destination host
- Authentication result
- Event timestamp
- SSH process information

The detection query was built based on the actual event format instead of assuming that all fields would be extracted automatically.

## 3. Field Extraction Improves Investigation

Some useful information was contained inside the raw event text and required extraction using SPL commands such as `rex`.

Extracting fields made it easier to:

- Group events by source IP
- Count failed login attempts
- Identify targeted usernames
- Compare failed and successful authentications
- Display useful information in dashboards

## 4. Detection Thresholds Require Testing

A brute-force detection needs a defined threshold and time window.

If the threshold is too low, normal login mistakes may create false positives.

If the threshold is too high, suspicious activity may not generate an alert.

Controlled testing with Kali Linux helped validate whether the detection condition worked as expected.

## 5. A Successful Login Changes the Severity

Repeated failed login attempts may indicate an unsuccessful brute-force attempt.

However, repeated failures followed by a successful login from the same source IP may indicate account compromise.

This sequence requires additional investigation and should generally receive a higher severity than failed attempts alone.

## 6. Alerts Need Investigation Context

An alert should provide enough information for an analyst to begin triage.

Useful alert fields include:

- Source IP address
- Destination host
- Targeted username
- Number of failed attempts
- First event time
- Last event time
- Authentication result

Including these fields reduces the amount of manual searching required during an investigation.

## 7. Dashboards Support Monitoring but Do Not Replace Investigation

Dashboards provide visibility into trends and suspicious activity, but they do not provide the complete context of an incident.

Analysts still need to review:

- Raw events
- Related successful authentications
- Activity before and after the alert
- Other actions performed by the source IP
- Possible false-positive explanations

## 8. Incident Documentation Is Part of the SOC Process

Writing an incident report helped organize the investigation into clear sections:

- Alert summary
- Evidence
- Classification
- Severity
- Indicators of compromise
- Recommended response actions

This made the investigation easier to review and communicate.

## 9. Controlled Testing Is Essential

The attack simulations were performed inside an isolated lab environment.

Controlled testing allowed the detection to be validated safely without affecting production systems or unauthorized devices.

## 10. Future Learning Areas

The project identified several areas for further improvement:

- Windows event log collection
- Sysmon deployment
- MITRE ATT&CK mapping
- Additional authentication detections
- Web attack monitoring
- GeoIP enrichment
- Automated response actions
- More advanced alert triage
- Detection tuning and false-positive reduction

## Conclusion

The Mini SOC lab demonstrated that effective detection depends on more than writing an SPL query.

A complete SOC workflow requires reliable log collection, detection testing, alert context, investigation, classification, and clear documentation.
