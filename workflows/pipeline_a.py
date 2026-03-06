"""Pipeline A: demo transcript to account memo and initial agent specification."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from workflows.utils import (
    ROOT_DIR,
    call_llm,
    get_output_path,
    parse_json_response,
    read_transcript,
    save_json,
)


EXTRACTION_PROMPT_PATH = ROOT_DIR / "prompts" / "extraction_prompt.txt"
AGENT_SPEC_PROMPT_PATH = ROOT_DIR / "prompts" / "agent_spec_prompt.txt"


def load_prompt(path: Path) -> str:
    """Load and return a prompt template from disk."""
    with path.open("r", encoding="utf-8") as file:
        return file.read()


def extract_account_memo(account_id: str, transcript: str) -> dict[str, Any]:
    """Extract a structured account memo from a demo transcript."""
    template = load_prompt(EXTRACTION_PROMPT_PATH)
    prompt = template.format(transcript=transcript)

    system = (
        "You extract accurate structured account setup details from transcripts. "
        "Output only strict JSON and never fabricate missing details."
    )
    raw_response = call_llm(prompt=prompt, system=system)
    memo = parse_json_response(raw_response)

    memo["account_id"] = account_id
    memo["version"] = "v1"
    memo["source"] = "demo"
    memo.setdefault("questions_or_unknowns", [])

    return memo


def generate_agent_spec(account_memo: dict[str, Any]) -> dict[str, Any]:
    """Generate the Retell agent specification JSON from an account memo."""
    template = load_prompt(AGENT_SPEC_PROMPT_PATH)
    prompt = template.format(account_memo=json.dumps(account_memo, indent=2))

    system = (
        "You generate production-ready Retell agent configuration JSON from account memos. "
        "Return only valid JSON."
    )
    raw_response = call_llm(prompt=prompt, system=system)
    agent_spec = parse_json_response(raw_response)

    agent_spec.setdefault("agent_name", f"{account_memo.get('company_name') or account_memo['account_id']} Agent")
    agent_spec["version"] = "v1"

    return agent_spec


def run_pipeline_a(account_id: str) -> bool:
    """Run Pipeline A for one account and return success status."""
    try:
        transcript_path = ROOT_DIR / "data" / "demo" / f"{account_id}_demo.txt"
        transcript = read_transcript(transcript_path)

        account_memo = extract_account_memo(account_id=account_id, transcript=transcript)
        agent_spec = generate_agent_spec(account_memo=account_memo)

        memo_output_path = get_output_path(account_id, "v1", "account_memo.json")
        spec_output_path = get_output_path(account_id, "v1", "agent_spec.json")

        save_json(account_memo, memo_output_path)
        save_json(agent_spec, spec_output_path)

        company_name = account_memo.get("company_name") or "Unknown Company"
        open_questions = len(account_memo.get("questions_or_unknowns", []))
        print(
            f"[Pipeline A] {account_id}: company='{company_name}', "
            f"open_questions={open_questions}"
        )
        return True
    except Exception as exc:
        print(f"[Pipeline A] {account_id} failed: {exc}")
        return False
