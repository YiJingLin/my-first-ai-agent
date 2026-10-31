# 3_financial_researcher

## What's new

Compared with `2_researcher`:

- `SerperDevTool` on the researcher via `tools=[SerperDevTool()]`
- `SERPER_API_KEY` in `.env`
- Analysis task YAML sets `context: [research_task]` so that task is passed in explicitly
- `output_file: output/report.md` on the analysis task in `tasks.yaml` (the reference also sets it again in `crew.py`)
- `input()` for the company name, plus `current_date` in `kickoff` inputs

Reference: https://github.com/ed-donner/agents/tree/main/3_crewai/reference/financial_researcher

## Create

```bash
cd 4_crewai/3_financial_researcher
crewai create crew financial_researcher
```

Put `OPENAI_API_KEY` and `SERPER_API_KEY` in `financial_researcher/.env`.

## Run

```bash
cd financial_researcher
crewai install
crewai run
```
