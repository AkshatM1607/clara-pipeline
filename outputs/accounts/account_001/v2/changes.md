# Changes

## Account Memo Diff (v1 -> v2)

- `after_hours_flow_summary`: `Ask if it is emergency, transfer emergencies to on-call line, otherwise capture details for next business day` -> `collect details and offer next-business-day morning or afternoon callback slot`
- `business_hours.end`: `6:00 PM` -> `6:30 PM`
- `business_hours.start`: `8:00 AM` -> `7:30 AM`
- `call_transfer_rules.message_if_fails`: `We did not reach a dispatcher yet, but we are logging your request now.` -> `We are escalating this now and a fire protection specialist will call you shortly`
- `call_transfer_rules.retries`: `2` -> `1`
- `call_transfer_rules.timeout_seconds`: `22` -> `28`
- `emergency_definition`: `['Active fire alarm trouble', 'Sprinkler burst', 'No water pressure to suppression lines', 'A downed fire pump']` -> `['panel showing supervisory fault at a hospital site']`
- `emergency_routing_rules.fallback`: `On-call tech line` -> `callback within 7 minutes`
- `emergency_routing_rules.order`: `['Megan Holt', 'Luis Pena', 'On-call tech line']` -> `['Luis Pena', 'Megan Holt', 'on-call tech line']`
- `emergency_routing_rules.primary_contact`: `Megan Holt` -> `Luis Pena`
- `integration_constraints`: `['No outbound SMS', 'No calendar writes from the agent', 'Housecall Pro']` -> `['Housecall Pro', 'no attachment uploads from the agent']`
- `non_emergency_routing_rules`: `Collect issue details and book with the service coordinator queue` -> `collect details and include preferred contact window`
- `notes`: `Keep tone calm because many callers are stressed facility managers.` -> `keep it concise and confident`
- `questions_or_unknowns`: `[]` -> `['other services supported', 'full emergency definition list', 'office hours flow details']`
- `services_supported`: `['Fire sprinkler inspection', 'Alarm panel testing', 'Extinguisher service', 'Code compliance checks']` -> `['backflow prevention testing']`
