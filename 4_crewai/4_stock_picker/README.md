# 4_stock_picker

## What's new

Compared with `3_financial_researcher`:

- `Process.hierarchical` with a `manager` agent (`allow_delegation=True`) passed as `manager_agent`
- `output_pydantic` on the find and research tasks (`TrendingCompanyList`, `TrendingCompanyResearchList`)
- `memory=True` on the worker agents and on the crew
- Custom tool: `@tool` in `tools/push_tool.py` (`send_push_notification`), using `PUSHOVER_USER` and `PUSHOVER_TOKEN`
- `SerperDevTool` stays on the finder and researcher
- Inputs are fixed in `main.py` (`sector=Technology`, `current_date`), not `input()`

Reference: https://github.com/ed-donner/agents/tree/main/3_crewai/reference/stock_picker

## Create

```bash
cd 4_crewai/4_stock_picker
crewai create crew stock_picker
```

Put `OPENAI_API_KEY`, `SERPER_API_KEY`, `PUSHOVER_USER`, and `PUSHOVER_TOKEN` in `stock_picker/.env`.

## Run

```bash
cd stock_picker
crewai install
crewai run
```
