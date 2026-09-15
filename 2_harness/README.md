# Prompt harness

Career twin with offline evaluation probes and a live policy gate (refuse unrelated / suspicious / dangerous asks).

## Prerequisites

- Parent `.env` with `OPENAI_API_KEY`
- `summary.txt` (and optional `linkedin.pdf`) in this folder
- Python 3.13 + venv (see below)

## Project structure

```
2_harness/
  harness_app.ipynb  # lab walkthrough (notebook + offline harness)
  harness_app.py     # Gradio entrypoint (gated chat)
  agent/
    __init__.py
    context.py       # loads summary/LinkedIn and builds the system prompt
    tools.py         # tool functions, JSON schemas, and tool-call handler
    runtime.py       # raw twin OpenAI chat loop
    policy.py        # classify / judge / gated chat
    harness.py       # curated cases + run_harness()
  tests/             # unit tests for agent/ (mocked OpenAI — no API key)
  pytest.ini         # pythonpath + testpaths for local/CI pytest
  summary.txt
  linkedin.pdf       # optional; gitignored
  requirements.txt
```

## Lab in Jupyter Notebook

`harness_app.ipynb` — same flow as the scripts, step by step (includes offline `run_harness()` probes).

## Run Python Script

From this folder, use a virtual environment (required on Homebrew Python):

```bash
cd 2_harness
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python harness_app.py
```

This launches Gradio with the live input/output policy gate.

If Gradio fails with a NumPy/`_multiarray_umath` error, run `unset PYTHONPATH` first — a global Homebrew `PYTHONPATH` in `~/.zshrc` can override the venv.

### Flow (`harness_app.py`)

```mermaid
flowchart TD
  A[harness_app.py: load_env → build_gated_chat → Gradio] --> B[User message]
  B --> C[classify_user_message — policy.py]
  C --> D["log: [gate] input category=…"]
  D --> E{on_topic?}

  E -->|no| F[Return REFUSAL]
  E -->|yes| G[generate_reply — runtime.py<br/>tools + context system prompt]
  G --> H[judge_reply — policy.py]
  H --> I{pass?}

  I -->|yes| J[Return reply to Gradio]
  I -->|no| K["log: [gate] output blocked → return blocked message"]
```

## Unit tests

Agent unit tests live under `tests/` (context, tools, runtime, policy, harness). They mock the OpenAI client — no `OPENAI_API_KEY` required. The same suite runs on PRs via GitHub Actions (`unit-tests.yml` matrix).

```bash
cd 2_harness
source .venv/bin/activate
unset PYTHONPATH   # if a global PYTHONPATH interferes
pip install -r requirements.txt   # includes pytest
python -m pytest tests/ -v
```

Useful variants:

```bash
python -m pytest tests/test_policy.py          # one file
python -m pytest tests/test_harness.py::test_run_harness_aggregates_mocked_verdicts
```

## Deployment

This project does not cover deployment. If you want to deploy a Gradio twin (Hugging Face Spaces or Render), follow the steps in [`../1_profile_chatbot/`](../1_profile_chatbot/).
