# TODO

Track follow-ups for this repo. Check items off when done (`[ ]` → `[x]`).
Once finished, tag on finish date in front of the item.

## PR checks

- [ ] Setup general PR check across projects (not only `1_profile_chatbot`; e.g. shared workflow pattern / jobs per project as tests land)
- [ ] Setup Ruleset to block PR merge whenever a required check failed (require status check `1_profile_chatbot pytest` on `main`)
- [ ] When ~5+ labs have `tests/`: decide whether to enhance GHA so PRs only run pytest for **changed** projects (path filters / change detection); keep a full run on `main`. Reminder also in `.github/workflows/*.yml` header comments.

## Design / next lab

- [ ] Setup new project for `agents/2_openai/1_lab1.ipynb` contents (scaffold folder, agent package, entrypoint, README — similar to `1_profile_chatbot` / `2_harness`), showing trace on OpenAI dashboard
- [ ] Multiple agents run parallel runs using async
- [ ] Agent orchestrating via code / LLM - either orchestrate via code or LLM. moreover, LLM provude agents as tool or handoff.