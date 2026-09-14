# TODO

Track follow-ups for this repo. Check items off when done (`[ ]` → `[x]`).
Once f

## PR checks

- [ ] Setup general PR check across projects (not only `1_profile_chatbot`; e.g. shared workflow pattern / jobs per project as tests land)
- [ ] Setup Ruleset to block PR merge whenever a required check failed (require status check `1_profile_chatbot pytest` on `main`)

## Design / next lab

- [ ] Setup new project for `agents/2_openai/1_lab1.ipynb` contents (scaffold folder, agent package, entrypoint, README — similar to `1_profile_chatbot` / `2_harness`)

## Cleanup (optional)

- [x] Remove intentional failing test `1_profile_chatbot/tests/test_intentional_fail.py` and push so the open PR check goes green again
