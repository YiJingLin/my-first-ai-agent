# OpenAI Agents SDK

Practice lab for the [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) (`openai-agents` on PyPI). Merges Week 2 course notebooks:

- [1_lab1.ipynb](https://github.com/ed-donner/agents/blob/main/2_openai/1_lab1.ipynb) — Agent, Runner, traces, tools, sessions
- [2_lab2.ipynb](https://github.com/ed-donner/agents/blob/main/2_openai/2_lab2.ipynb) — multi-agent orchestration (code + LLM)
- [3_lab3.ipynb](https://github.com/ed-donner/agents/blob/main/2_openai/3_lab3.ipynb) — other models, structured outputs, guardrails

## Prerequisites

- Parent `.env` with `OPENAI_API_KEY`
- Optional: `PUSHOVER_USER` / `PUSHOVER_TOKEN` for notify tools; `GOOGLE_API_KEY` for Stage 7 (Gemini)
- Python 3.13 + venv (see below)

Install the SDK as `openai-agents` — not the unrelated `agents` package on PyPI.

## Project structure

```
3_openai_agent/
  openai_agent.ipynb  # staged walkthrough (main lab for now)
  README.md
```

Package modules (`agent/`), a script entrypoint, `requirements.txt`, and tests will land as stages move out of the notebook.

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
pip install openai-agents python-dotenv
# open openai_agent.ipynb and select this venv as the kernel
```

If a global Homebrew `PYTHONPATH` interferes, run `unset PYTHONPATH` first.

## Unit tests

Not set up yet. When `tests/` lands, this lab can join the shared Actions matrix in `.github/workflows/unit-tests.yml`.
