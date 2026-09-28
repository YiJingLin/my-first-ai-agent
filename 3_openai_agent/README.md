# OpenAI Agents SDK

Practice lab for the [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) (`openai-agents` on PyPI). Merges Week 2 course notebooks:

- [1_lab1.ipynb](https://github.com/ed-donner/agents/blob/main/2_openai/1_lab1.ipynb) — Agent, Runner, traces, tools, sessions
- [2_lab2.ipynb](https://github.com/ed-donner/agents/blob/main/2_openai/2_lab2.ipynb) — multi-agent orchestration (code + LLM)
- [3_lab3.ipynb](https://github.com/ed-donner/agents/blob/main/2_openai/3_lab3.ipynb) — other models, structured outputs, guardrails

The Gradio product on top of those stages is **Sales Email Studio**: a Sales Manager chat that collects a brief, then drafts three styles in parallel and picks one.

## Prerequisites

- Parent `.env` with `OPENAI_API_KEY`
- Optional: `PUSHOVER_USER` / `PUSHOVER_TOKEN` for notify tools; `GOOGLE_API_KEY` for Stage 7 (Gemini)
- Python 3.13 + venv (see below)

Install the SDK as `openai-agents` — not the unrelated `agents` package on PyPI.

## Project structure

```
3_openai_agent/
  openai_agent.ipynb  # staged walkthrough
  app.py              # Gradio Sales Email Studio
  agent/
    brief.py          # EmailBrief + merge across turns
    agents.py         # 6 Agent constructors
    guardrails.py     # intake tripwire + SDK @input_guardrail
    orchestrate.py    # turn: intake → ask or gather + pick
    runtime.py        # load_env, MODEL
  tests/              # brief merge + incomplete brief blocks writers
  requirements.txt
  README.md
```

## Sales Email Studio

Six agents; only the Sales Manager talks to the user.

1. **Intake Checker** extracts `author`, `receiver`, `field`, `purpose` into `EmailBrief`.
2. If the brief is incomplete, the Manager asks for `missing_fields` — writers do not run.
3. Once complete: Friendly / Professional / Creative writers run in parallel (`asyncio.gather`), then **Draft Picker** chooses the draft the Manager presents.

Writers and the picker also carry an `@input_guardrail` that trips if `RunContext.brief` is incomplete.

```bash
cd 3_openai_agent
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

If Gradio fails with a NumPy/`_multiarray_umath` error, run `unset PYTHONPATH` first.

## Practice arc

Work the stages in `openai_agent.ipynb` in order:

| Stage | Focus | Checkpoint |
|------|--------|------------|
| 1 | SDK hello — `Agent` + `Runner` | One agent reply works |
| 2 | Observability + streaming | Trace on [OpenAI traces](https://platform.openai.com/traces) |
| 3 | Function tools (`@function_tool`) | Tool call visible in the trace |
| 4 | Memory / sessions | Name remembered across two `Runner.run` calls |
| 5 | Orchestrate by code | Parallel drafts → picker (optional send) |
| 6 | Orchestrate by LLM | Manager via agents-as-tools, then handoffs |
| 7 | Other providers / models | Non-OpenAI model (e.g. Gemini) via OpenAI-compatible client |
| 8 | Structured outputs | `final_output` is a Pydantic object |
| 9 | Guardrails | DIY checker and/or SDK `@output_guardrail` |

Delivery (email/SMTP) is optional. Prefer Pushover or a dry-run print tool so the focus stays on agents. Sandbox agents and MCP stay stretch-only in the notebook.

## Lab in Jupyter Notebook

From this folder:

```bash
cd 3_openai_agent
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# open openai_agent.ipynb and select this venv as the kernel
```

If a global Homebrew `PYTHONPATH` interferes, run `unset PYTHONPATH` first.

## Unit tests

```bash
cd 3_openai_agent
source .venv/bin/activate
unset PYTHONPATH   # if a global PYTHONPATH interferes
pip install -r requirements.txt
python -m pytest tests/ -v
```

Tests mock agent runs — no `OPENAI_API_KEY` required. The suite is on the shared Actions matrix in `.github/workflows/unit-tests.yml`.
