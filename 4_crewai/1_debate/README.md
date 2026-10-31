# 1_debate

Baseline crew. Later labs add to this.

## What's new

- `crewai create crew` scaffold: `src/debate/crew.py`, `config/agents.yaml`, `config/tasks.yaml`, `main.py`
- `@CrewBase`, `@agent`, `@task`, `@crew`
- `Process.sequential`
- `{motion}` filled by `kickoff(inputs=...)`; `main.py` reads the motion with `input()`
- One `debater` agent on both the propose and oppose tasks, then a separate `judge`
- `output_file` on each task in `tasks.yaml` (`output/propose.md`, `output/oppose.md`, `output/decide.md`)
- `verbose=True` and `tracing=True` on the crew

Reference: `agents/3_crewai/reference/debate`

## Create

```bash
cd 4_crewai/1_debate
crewai create crew debate
```

Put `OPENAI_API_KEY` in `debate/.env`.

## Run

```bash
cd debate
crewai install
crewai run
```
