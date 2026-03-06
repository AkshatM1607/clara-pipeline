# clara-pipeline

Automation pipeline for configuring Clara Answers AI voice agents for service trade businesses.

## What this project does

This project runs two local JSON-based pipelines:

- Pipeline A: Demo call transcript -> structured account memo -> Retell agent config (`v1`)
- Pipeline B: Onboarding call transcript -> changes detected -> merged account memo -> updated agent config (`v2`) + changelog

## Tech stack

- Python 3
- Groq API (`llama3-70b-8192`)
- Libraries: `groq`, `python-dotenv`
- Storage: local JSON files only

## Project structure

```text
clara-pipeline/
  .env.example
  .gitignore
  requirements.txt
  README.md
  run_all.py

  workflows/
    utils.py
    pipeline_a.py
    pipeline_b.py

  prompts/
    extraction_prompt.txt
    agent_spec_prompt.txt

  data/
    demo/
    onboarding/

  outputs/
    accounts/
```

## Setup

1. Create and activate a Python environment (recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create `.env` from `.env.example` and set your key:

```env
GROQ_API_KEY=your_real_groq_api_key
```

## Run

From the project root:

```bash
python run_all.py
```

The script will:

- Discover accounts by scanning `data/demo/*_demo.txt`
- Run Pipeline A for each account
- Run Pipeline B only when `data/onboarding/{account_id}_onboarding.txt` exists
- Continue processing even if one account fails
- Print a summary table:

```text
Account | Pipeline A | Pipeline B
```

## Outputs

For each account, outputs are written to:

- `outputs/accounts/{account_id}/v1/account_memo.json`
- `outputs/accounts/{account_id}/v1/agent_spec.json`
- `outputs/accounts/{account_id}/v2/account_memo.json`
- `outputs/accounts/{account_id}/v2/agent_spec.json`
- `outputs/accounts/{account_id}/v2/changes.md`

All output paths are built with `get_output_path(account_id, version, filename)`.

## Reliability notes

- No API keys are hardcoded.
- LLM JSON responses are always parsed via `parse_json_response()`.
- JSON parsing supports both raw JSON and ```json fenced output.
- All file writes auto-create parent directories.
- `run_pipeline_a()` and `run_pipeline_b()` return `True`/`False` and do not crash caller execution.
- `run_all.py` continues across account failures.
