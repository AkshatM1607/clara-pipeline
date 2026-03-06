# Changes

## Account Memo Diff (v1 -> v2)

- `after_hours_flow_summary`: `Ask emergency yes or no, transfer emergency calls to overnight duty phone, otherwise log details for morning dispatch` -> `Emergency calls transfer to overnight duty phone; non-emergency should offer first-available next-day slot preference`
- `business_hours.days`: `Monday to Saturday` -> `Monday to Sunday`
- `business_hours.end`: `7:00 PM` -> `8:00 PM`
- `business_hours.start`: `7:30 AM` -> `7:00 AM`
- `call_transfer_rules.message_if_fails`: `We are still connecting you, please hold while we secure the right specialist` -> `We have your urgent request and our dispatch team will reach out very soon`
- `call_transfer_rules.retries`: `2` -> `3`
- `call_transfer_rules.timeout_seconds`: `20` -> `24`
- `emergency_definition`: `['No cooling above 95 degrees', 'no heat below 40 degrees', 'burning smell from unit', 'refrigerant leak concerns']` -> `['carbon monoxide alarm tied to HVAC equipment']`
- `emergency_routing_rules.fallback`: `Tell callers we flagged urgent status and a technician will return call in 15 minutes` -> `callback promise is 10 minutes`
- `emergency_routing_rules.order`: `['Carla Nguyen', 'Omar Reed', 'priority technician ring group']` -> `['Omar Reed', 'Carla Nguyen', 'priority technician ring group']`
- `emergency_routing_rules.primary_contact`: `Carla Nguyen` -> `Omar Reed`
- `integration_constraints`: `['ServiceTitan only', 'no payment collection', 'no warranty promises']` -> `['ServiceTitan only', 'do not discuss financing options']`
- `non_emergency_routing_rules`: `Gather issue type and preferred window, then queue for scheduler callback` -> `scheduler callback, gather if customer is new or existing`
- `notes`: `Keep it direct and reassuring` -> `Communication style: Warm but fast-paced`
- `services_supported`: `['AC repair', 'furnace tune-ups', 'duct cleaning', 'thermostat replacement']` -> `['indoor air quality diagnostics']`
