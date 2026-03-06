# Changes

## Account Memo Diff (v1 -> v2)

- `after_hours_flow_summary`: `Confirm emergency, route urgent calls to on-call electrician, non-urgent gets a next-day callback ticket` -> `Emergency transfers to on-call electrician, non-emergency gets ticket plus preferred callback time`
- `business_hours.days`: `Monday through Friday` -> `Monday through Saturday`
- `business_hours.end`: `5:30 PM` -> `6:00 PM`
- `business_hours.start`: `8:00 AM` -> `7:00 AM`
- `call_transfer_rules.message_if_fails`: `We are lining up the right electrician now and will stay with you` -> `We are escalating to our electrical response team and you are in priority queue`
- `call_transfer_rules.retries`: `3` -> `2`
- `call_transfer_rules.timeout_seconds`: `18` -> `21`
- `emergency_definition`: `['Burning odor', 'smoking panel', 'total power loss in occupied site', 'sparking outlet']` -> `['repeated breaker trip in medical office']`
- `emergency_routing_rules.fallback`: `we are alerting the on-call electrician and they should expect callback in under 12 minutes` -> `callback within 9 minutes`
- `emergency_routing_rules.order`: `['Erin Blake', 'Dante Ruiz', 'emergency electrician hotline']` -> `['Dante Ruiz', 'Erin Blake', 'emergency electrician hotline']`
- `emergency_routing_rules.primary_contact`: `Erin Blake` -> `Dante Ruiz`
- `integration_constraints`: `['We use Jobber; do not quote prices and do not book permit-related jobs automatically']` -> `['Jobber limits', 'no permit timeline guarantees']`
- `non_emergency_routing_rules`: `Gather caller info and problem summary, then send to front desk scheduling queue` -> `collect details, capture if tenant or property owner`
- `notes`: `Keep it calm and safety-focused` -> `Be calm and safety-forward, not technical`
- `services_supported`: `['Panel upgrades', 'breaker troubleshooting', 'lighting retrofits', 'EV charger installs']` -> `['standby generator diagnostics']`
