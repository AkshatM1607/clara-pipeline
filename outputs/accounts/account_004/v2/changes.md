# Changes

## Account Memo Diff (v1 -> v2)

- `after_hours_flow_summary`: `Ask if emergency, transfer emergencies to on-call plumber, non-emergency leaves service details for morning` -> `Emergency transfers remain, non-emergency should collect details and ask preferred callback window tomorrow`
- `business_hours.end`: `9:00 PM` -> `10:00 PM`
- `business_hours.start`: `6:00 AM` -> `5:30 AM`
- `call_transfer_rules.message_if_fails`: `We are securing the next available plumber and will contact you shortly` -> `We are dispatching the next available plumber and will call you shortly with status`
- `call_transfer_rules.retries`: `2` -> `1`
- `call_transfer_rules.timeout_seconds`: `25` -> `30`
- `emergency_definition`: `['Major leak flooding', 'Sewer backup', 'No water in occupied home', 'Burst pipe']` -> `['gas line leak with odor']`
- `emergency_routing_rules.fallback`: `Tell caller help is being escalated and plumber callback target is 20 minutes` -> `12 minutes`
- `emergency_routing_rules.order`: `['Dispatch captain Nora Patel', 'Operations lead Ben Chavez', 'Emergency plumber group line']` -> `['Ben Chavez', 'Nora Patel', 'emergency plumber group line']`
- `emergency_routing_rules.primary_contact`: `Dispatch captain Nora Patel` -> `Ben Chavez`
- `integration_constraints`: `['FieldEdge integration only', 'No insurance claim advice', 'No parts cost commitments']` -> `['FieldEdge only', 'do not provide insurance coverage guidance']`
- `non_emergency_routing_rules`: `Collect details and place into standard scheduling queue` -> `standard scheduling queue and collect whether water must be shut off`
- `notes`: `Keep language simple for homeowners` -> `Keep it plain language and empathetic`
- `services_supported`: `['Drain cleaning', 'Leak detection', 'Water heater repair', 'Sewer camera inspections']` -> `['slab leak inspection']`
