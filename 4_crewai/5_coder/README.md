# 5_coder

## What's new

Compared with `4_stock_picker`:

- Back to `Process.sequential`, one agent, one task
- No manager, memory, `output_pydantic`, Serper, or Pushover
- Sandbox tools in `tools/sandbox_tools.py`: list, read, write, and run a Python file
- Run tool executes the file in Docker (`python:3.13-slim`). Docker Desktop has to be running
- `cache_function` on those tools returns `False` so CrewAI does not cache sandbox results
- `{assignment}` comes from a string in `main.py`. The reference assignment sums the Leibniz series (1,000,000 terms) and multiplies by 4

Reference: https://github.com/ed-donner/agents/tree/main/3_crewai/reference/coder

## Create

```bash
cd 4_crewai/5_coder
crewai create crew coder
```

Put `OPENAI_API_KEY` in `coder/.env`.

## Run

```bash
cd coder
crewai install
crewai run
```
