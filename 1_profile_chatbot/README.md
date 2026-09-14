# Profile Chatbot
This first project is to create a profile/career chatbot.
1. The chatbot will use OpenAI API as LLM backend.
2. During conversation, the LLM will decide whether call the tooling function we define.
3. Lastly, we are able to deploy the chatbot to Hugging Face Spaces (or Render).

ref: https://github.com/ed-donner/agents/blob/main/1_foundations/4_lab4.ipynb

Policy harness / live gate: see `../2_harness/`.

## Prerequisites

- Parent `.env` with `OPENAI_API_KEY`
- Python 3.13 + venv (see Run Python Script below)
- Download `linkedin.pdf` from your LinkedIn profile page (optional)
- Edit `summary.txt` about yourself

## Project Structure

```
1_profile_chatbot/
  README.md               # this file (local / GitHub docs)
  profile_chatbot.ipynb   # lab walkthrough (notebook)
  profile_chatbot.py      # local Gradio entrypoint
  sync_space.sh           # copies sources into space/ before deploy
  agent/
    __init__.py
    context.py            # loads summary/LinkedIn and builds the system prompt
    tools.py              # tool functions, JSON schemas, and tool-call handler
    runtime.py            # shared OpenAI chat loop (local + Space)
  tests/                  # unit tests for agent/ (mocked OpenAI — no API key)
  pytest.ini              # pythonpath + testpaths for local/CI pytest
  summary.txt
  linkedin.pdf            # optional; gitignored
  requirements.txt
  space/                  # Hugging Face deploy root only
    README.md             # HF Spaces YAML config (not this project's docs)
    app.py                # Space entrypoint (sdk app_file)
    .gitignore            # ignores files filled in by sync_space.sh
```

### Lab in Jupyter Notebook

`profile_chatbot.ipynb` — same agent flow as the scripts, step by step.

## Run Python Script

From this folder, use a virtual environment (required on Homebrew Python):

```bash
cd 1_profile_chatbot
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python profile_chatbot.py
```

If Gradio fails with a NumPy/`_multiarray_umath` error, run `unset PYTHONPATH` first — a global Homebrew `PYTHONPATH` in `~/.zshrc` can override the venv.

## Unit tests

Agent unit tests live under `tests/`. They mock the OpenAI client — no `OPENAI_API_KEY` required. The same suite runs on PRs via GitHub Actions.

```bash
cd 1_profile_chatbot
source .venv/bin/activate
unset PYTHONPATH   # if a global PYTHONPATH interferes
pip install -r requirements.txt   # includes pytest
python -m pytest tests/ -v
```

Useful variants:

```bash
python -m pytest tests/test_tools.py          # one file
python -m pytest tests/test_runtime.py::test_chat_runs_tool_loop_then_answers
```

## Deployment (Hugging Face Spaces)

Local `README.md` stays human docs. HF config lives only under `space/README.md`, so `gradio deploy` does not fight this file.

**Note:** As of July 2026, new Gradio Spaces on free HF accounts are restricted (CPU Basic / Gradio often needs PRO). If create fails on free tier, use the course’s Render guide at `agents/1_foundations/RENDER_INSTRUCTIONS.md` (sibling of `my-first-ai-agent/`): after `./sync_space.sh`, point Render at `space/` with start command `python app.py`.

### 1. Sync the Space folder

Always sync before deploy (copies `agent/`, `summary.txt`, `linkedin.pdf`, `requirements.txt` into `space/`):

```bash
cd 1_profile_chatbot
chmod +x sync_space.sh   # once
./sync_space.sh
```

Optional local smoke test of the Space entrypoint:

```bash
source .venv/bin/activate
unset PYTHONPATH
cd space && python app.py
```

### 2. Hugging Face login

1. Create an account at https://huggingface.co
2. Avatar → **Access Tokens** → create a token with **write** permission
3. From this project’s venv:

```bash
source .venv/bin/activate
hf auth login
# paste the write token when prompted
hf auth whoami
```

(Or: `hf auth login --token hf_xxx`. Optionally add `HF_TOKEN=hf_xxx` to the parent `.env`.)

### 3. Deploy

```bash
cd 1_profile_chatbot
./sync_space.sh
source .venv/bin/activate
cd space
gradio deploy
```

Because `space/README.md` already has Spaces YAML, deploy should **reuse** that config (title `Profile_Chatbot` / `Profile Chatbot`, `app_file: app.py`) and skip most first-time questions. It will create or update the Space with that title (`exist_ok`).

If you need the full interactive wizard again, temporarily move/rename `space/README.md`, run `gradio deploy`, then restore the YAML README if you want.

Course-equivalent with `uv` (optional): from `space/`, `uv run gradio deploy`.

### 4. Add secrets on the Space

1. Open https://huggingface.co/spaces → your Space
2. **Settings** → **Variables and secrets** → **New secret**
3. Add at least `OPENAI_API_KEY` (value from parent `.env`)
4. **Restart** the Space, then open the **App** tab and chat

Never commit `.env` or put API keys in `space/`.
