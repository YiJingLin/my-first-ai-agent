# CrewAI

Walk the course reference crews in [ed-donner/agents `3_crewai/reference`](https://github.com/ed-donner/agents/tree/main/3_crewai/reference) one folder at a time. Build each one inside the numbered lab below, and copy that lab's prompts from the matching reference when you wire agents and tasks.

The numbered folder is the lab. The CrewAI package is created inside it (`debate`, `researcher`, …) because a Python module name cannot start with a digit.

## Once per machine

From the repo root, use the same CLI version as the course reference:

```bash
uv tool list
uv tool uninstall crewai   # only if an older or newer crewai tool is already installed
uv tool install crewai==1.14.4
uv tool list
```

`crewai create crew` on 1.14.4 scaffolds `crew.py` plus `config/agents.yaml` and `config/tasks.yaml`, which is what these labs follow.

Each new project gets its own `.env`. Start with `OPENAI_API_KEY`. Later labs add keys in that lab's README.

## Labs

1. `1_debate`
2. `2_researcher`
3. `3_financial_researcher`
4. `4_stock_picker`
5. `5_coder`
6. `6_engineering_team`

`5_coder` and `6_engineering_team` need Docker Desktop running before `crewai run`.
