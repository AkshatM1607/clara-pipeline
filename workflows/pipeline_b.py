"""Pipeline B: onboarding transcript to merged memo, updated agent specification, and changelog."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from workflows.utils import (
    ROOT_DIR,
    call_llm,
    get_output_path,
    load_json,
    parse_json_response,
    read_transcript,
    save_json,
    save_text,
)


EXTRACTION_PROMPT_PATH = ROOT_DIR / "prompts" / "extraction_prompt.txt"
AGENT_SPEC_PROMPT_PATH = ROOT_DIR / "prompts" / "agent_spec_prompt.txt"


PROTECTED_KEYS = {"account_id", "version", "source"}


def load_prompt(path: Path) -> str:
    """Load and return a prompt template from disk."""
    with path.open("r", encoding="utf-8") as file:
        return file.read()


def extract_onboarding_updates(account_id: str, transcript: str) -> dict[str, Any]:
    """Extract updated account details from onboarding transcript text."""
    template = load_prompt(EXTRACTION_PROMPT_PATH)
    prompt = template.format(transcript=transcript)

    system = (
        "You extract updated account setup details from onboarding transcripts. "
        "Return only strict JSON and keep uncertain details in questions_or_unknowns."
    )
    raw_response = call_llm(prompt=prompt, system=system)
    updates = parse_json_response(raw_response)

    updates["account_id"] = account_id
    updates["version"] = "v2"
    updates["source"] = "onboarding"
    updates.setdefault("questions_or_unknowns", [])

    return updates


def _merge_values(base_value: Any, update_value: Any, key: str | None = None) -> Any:
    """Merge two values recursively while honoring protected keys and null semantics."""
    if key in PROTECTED_KEYS:
        return base_value

    if update_value is None:
        return base_value

    if isinstance(base_value, dict) and isinstance(update_value, dict):
        merged: dict[str, Any] = dict(base_value)
        for sub_key, sub_val in update_value.items():
            if sub_key in merged:
                merged[sub_key] = _merge_values(merged[sub_key], sub_val, key=sub_key)
            else:
                if sub_key not in PROTECTED_KEYS and sub_val is not None:
                    merged[sub_key] = sub_val
        return merged

    if isinstance(base_value, list) and isinstance(update_value, list):
        if not update_value:
            return base_value
        return update_value

    return update_value


def merge_memo(base_memo: dict[str, Any], onboarding_updates: dict[str, Any]) -> dict[str, Any]:
    """Merge onboarding updates into v1 memo without overwriting protected keys."""
    merged = dict(base_memo)
    for key, value in onboarding_updates.items():
        if key in PROTECTED_KEYS:
            continue
        if key in merged:
            merged[key] = _merge_values(merged[key], value, key=key)
        elif value is not None:
            merged[key] = value

    merged["account_id"] = base_memo.get("account_id")
    merged["version"] = "v2"
    merged["source"] = base_memo.get("source", "demo")

    return merged


def generate_agent_spec_v2(account_memo: dict[str, Any]) -> dict[str, Any]:
    """Generate the v2 Retell agent specification from the merged memo."""
    template = load_prompt(AGENT_SPEC_PROMPT_PATH)
    prompt = template.format(account_memo=json.dumps(account_memo, indent=2))

    system = (
        "You generate production-ready Retell agent configuration JSON from account memos. "
        "Return only valid JSON."
    )
    raw_response = call_llm(prompt=prompt, system=system)
    agent_spec = parse_json_response(raw_response)

    agent_spec.setdefault("agent_name", f"{account_memo.get('company_name') or account_memo['account_id']} Agent")
    agent_spec["version"] = "v2"

    return agent_spec


def _flatten_dict(data: Any, prefix: str = "") -> dict[str, Any]:
    """Flatten nested dictionaries and lists to dot-notated key-value pairs."""
    flattened: dict[str, Any] = {}

    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            flattened.update(_flatten_dict(value, new_prefix))
        return flattened

    flattened[prefix] = data
    return flattened


def generate_changelog(v1_memo: dict[str, Any], v2_memo: dict[str, Any]) -> str:
    """Generate a markdown changelog describing memo changes from v1 to v2."""
    flat_v1 = _flatten_dict(v1_memo)
    flat_v2 = _flatten_dict(v2_memo)

    keys = sorted(set(flat_v1.keys()) | set(flat_v2.keys()))
    changes: list[str] = []

    for key in keys:
        if key in PROTECTED_KEYS:
            continue
        old = flat_v1.get(key, "<missing>")
        new = flat_v2.get(key, "<missing>")
        if old != new:
            changes.append(f"- `{key}`: `{old}` -> `{new}`")

    if not changes:
        changes.append("- No differences detected between v1 and v2 memos.")

    lines = [
        "# Changes",
        "",
        "## Account Memo Diff (v1 -> v2)",
        "",
        *changes,
        "",
    ]
    return "\n".join(lines)


def run_pipeline_b(account_id: str) -> bool:
    """Run Pipeline B for one account and return success status."""
    try:
        v1_memo_path = get_output_path(account_id, "v1", "account_memo.json")
        if not v1_memo_path.exists():
            raise FileNotFoundError(
                f"Missing v1 memo for {account_id}. Run Pipeline A first."
            )

        onboarding_path = ROOT_DIR / "data" / "onboarding" / f"{account_id}_onboarding.txt"
        transcript = read_transcript(onboarding_path)

        v1_memo = load_json(v1_memo_path)
        onboarding_updates = extract_onboarding_updates(account_id=account_id, transcript=transcript)
        v2_memo = merge_memo(base_memo=v1_memo, onboarding_updates=onboarding_updates)
        v2_agent_spec = generate_agent_spec_v2(account_memo=v2_memo)
        changes_md = generate_changelog(v1_memo=v1_memo, v2_memo=v2_memo)

        save_json(v2_memo, get_output_path(account_id, "v2", "account_memo.json"))
        save_json(v2_agent_spec, get_output_path(account_id, "v2", "agent_spec.json"))
        save_text(changes_md, get_output_path(account_id, "v2", "changes.md"))

        print(f"[Pipeline B] {account_id}: generated v2 memo/spec and changelog")
        return True
    except Exception as exc:
        print(f"[Pipeline B] {account_id} failed: {exc}")
        return False
