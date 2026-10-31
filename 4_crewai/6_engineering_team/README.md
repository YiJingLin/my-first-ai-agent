# 6_engineering_team

## What's new

Compared with `5_coder`:

- Four sequential agents: engineering lead, backend engineer, frontend engineer, test engineer
- Later tasks set `context:` to earlier tasks (`design_task`, then `code_task`)
- Same sandbox tool names, but run uses `uv run` inside `ghcr.io/astral-sh/uv:python3.13-bookworm-slim`
- `reset_sandbox()` before `kickoff`: deletes the sandbox, `uv init`, then `uv add gradio`
- `mcps=["https://mcp.context7.com/mcp"]` on the engineering lead and the frontend engineer
- `import engineering_team.patch` before creating the crew (CrewAI 1.14.4 MCP tool names that contain hyphens)
- Engineering lead `llm` is `openai/gpt-5.5`. The other agents stay on `openai/gpt-5.4-mini`
- Requirements string in `main.py` is a trading-account simulator (deposit, withdraw, buy, sell, holdings, P&L)

Reference: `agents/3_crewai/reference/engineering_team`

## Create

```bash
cd 4_crewai/6_engineering_team
crewai create crew engineering_team
```

Put `OPENAI_API_KEY` in `engineering_team/.env`. Docker Desktop has to be running.

## Run

```bash
cd engineering_team
crewai install
crewai run
```
