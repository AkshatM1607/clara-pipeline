# Changes

## Account Memo Diff (v1 -> v2)

- `after_hours_flow_summary`: `Confirm emergency status, transfer emergency to overnight monitoring desk, otherwise take details for next-day team` -> `Emergency transfers go to overnight monitoring desk; non-emergency should collect details and provide next-day callback expectation`
- `business_hours.days`: `Monday through Friday` -> `Monday through Saturday`
- `business_hours.end`: `6:30 PM` -> `7:00 PM`
- `business_hours.start`: `8:30 AM` -> `8:00 AM`
- `call_transfer_rules.message_if_fails`: `We are still attempting a secure handoff and your case is in active review` -> `Your security case is marked high priority and our monitoring lead will contact you shortly`
- `call_transfer_rules.retries`: `3` -> `2`
- `call_transfer_rules.timeout_seconds`: `19` -> `23`
- `emergency_definition`: `['Active break-in alarm', 'fire panel alarm on monitored site', 'access control lockout at critical facility', 'full camera outage at secured property']` -> `['forced door alarm at healthcare site']`
- `emergency_routing_rules.fallback`: `Reassure critical priority and response team calls back within 8 minutes` -> `6 minutes response callback target`
- `emergency_routing_rules.order`: `['Tasha Cole', 'Ian Ford', 'rapid response coordinator line']` -> `['Ian Ford', 'Tasha Cole', 'rapid response coordinator line']`
- `emergency_routing_rules.primary_contact`: `Tasha Cole` -> `Ian Ford`
- `integration_constraints`: `['Brivo and Alarm.com only; no remote unlock commands from voice agent']` -> `['Brivo', 'Alarm.com', 'no password reset actions by voice agent']`
- `non_emergency_routing_rules`: `Capture account ID and issue summary, then queue for support specialist callback` -> `Capture account ID, site name, and preferred callback number`
- `notes`: `Professional and confident, never alarmist` -> `Keep language calm, authoritative, and concise`
- `services_supported`: `['Alarm monitoring setup', 'camera installation', 'access control', 'smart sensor diagnostics']` -> `['intercom troubleshooting support']`
