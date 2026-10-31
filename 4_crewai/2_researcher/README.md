# 2_researcher

## What's new

Compared with `1_debate`:

- Two different agents (researcher, then reporting analyst) instead of one agent reused on two tasks
- `output_file` set in `crew.py` on the reporting `Task(...)`, not in `tasks.yaml`
- `kickoff` inputs are `topic` and `current_year` (no `input()` prompt)
- The second task receives the first task's output because the crew is sequential. There is still no `context:` list

Reference: https://github.com/ed-donner/agents/tree/main/3_crewai/reference/researcher

## Create

```bash
cd 4_crewai/2_researcher
crewai create crew researcher
```

Put `OPENAI_API_KEY` in `researcher/.env`.

## Run

```bash
cd researcher
crewai install
crewai run
```
