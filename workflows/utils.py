"""Utility helpers for Clara pipeline workflows."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from groq import Groq


ROOT_DIR = Path(__file__).resolve().parent.parent
MODEL_NAME = "llama-3.3-70b-versatile"


def get_groq_client() -> Groq:
    """Load environment variables and return an initialized Groq client."""
    load_dotenv(ROOT_DIR / ".env")
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "Missing GROQ_API_KEY. Add it to your .env file or environment variables."
        )
    return Groq(api_key=api_key)


def call_llm(prompt: str, system: str) -> str:
    """Call the Groq LLM with the configured model and return raw text output."""
    client = get_groq_client()
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.1,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError("LLM returned an empty response.")
    return content


def parse_json_response(raw: str) -> dict[str, Any]:
    """Parse JSON from raw LLM output, supporting fenced and unfenced JSON."""
    if raw is None:
        raise ValueError("LLM response is None; expected JSON text.")

    text = raw.strip()
    if not text:
        raise ValueError("LLM response is empty; expected JSON text.")

    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
        if text.lower().startswith("json"):
            text = text[4:].strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        preview = text[:400].replace("\n", " ")
        raise ValueError(
            f"Failed to parse JSON response: {exc.msg} at line {exc.lineno}, "
            f"column {exc.colno}. Response preview: {preview}"
        ) from exc

    if not isinstance(parsed, dict):
        raise ValueError("Parsed JSON must be an object at the top level.")

    return parsed


def save_json(data: dict[str, Any], path: Path | str) -> None:
    """Save dictionary data as pretty JSON and create parent directories if needed."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def load_json(path: Path | str) -> dict[str, Any]:
    """Load and return JSON object data from disk."""
    input_path = Path(path)
    with input_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_text(text: str, path: Path | str) -> None:
    """Save plain text to disk and create parent directories if needed."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        file.write(text)


def read_transcript(path: Path | str) -> str:
    """Read and return transcript text from a file path."""
    transcript_path = Path(path)
    with transcript_path.open("r", encoding="utf-8") as file:
        return file.read().strip()


def get_output_path(account_id: str, version: str, filename: str) -> Path:
    """Build an output path under outputs/accounts/{account_id}/{version}/."""
    return ROOT_DIR / "outputs" / "accounts" / account_id / version / filename
