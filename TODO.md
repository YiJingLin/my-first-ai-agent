# TODO

Track follow-ups for this repo. Check items off when done (`[ ]` → `[x]`).
Once finished, tag on finish date `[yyyy-mm-dd]` in front of the item.

## PR checks

- [x] [2026-09-15] Setup general PR check across projects (matrix in `.github/workflows/unit-tests.yml`; add labs to `matrix.project` as tests land)
- [ ] Setup Ruleset to block PR merge whenever a required check failed (require status checks `1_profile_chatbot pytest` and `2_guardrails pytest` on `main`)
- [ ] When ~5+ labs have `tests/`: decide whether to enhance GHA so PRs only run pytest for **changed** projects (path filters / change detection); keep a full run on `main`. Reminder also in `.github/workflows/*.yml` header comments.

## Naming / cleanup

- [x] [2026-09-20] Rename `2_harness` → `2_guardrails` (guardrails-first; demote offline probes; update README, entrypoints, CI matrix). If a Ruleset already requires `2_harness pytest`, switch it to `2_guardrails pytest`.

## Design / next lab

- [x] [2026-09-19] Setup new project for `agents/2_openai/1_lab1.ipynb` contents — landed as `3_openai_agent/` (notebook walkthrough + README; package/entrypoint can follow later)
- [ ] Multiple agents run parallel runs using async
- [ ] Agent orchestrating via code / LLM - either orchestrate via code or LLM. moreover, LLM provude agents as tool or handoff.