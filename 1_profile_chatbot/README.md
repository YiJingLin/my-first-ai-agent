# Profile Chatbot
This first project is to create a profile/career chatbot. 
1. The chatbot will use OpenAI API as LLM backend. 
2. During conversation, the LLM will decide whether call the tooling function we define. 
3. Lastly, we are able to deploy the chatbot to Hugging face as cloud service.

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
  profile_chatbot.ipynb   # lab walkthrough (notebook)
  profile_chatbot.py      # Gradio entrypoint: OpenAI chat loop + UI launch
  agent/
    __init__.py           # marks agent/ as a Python package
    context.py            # loads summary/LinkedIn and builds the system prompt
    tools.py              # tool functions, JSON schemas, and tool-call handler
  summary.txt             # short bio fed into the system prompt
  linkedin.pdf            # optional LinkedIn PDF for extra context
  requirements.txt        # Python dependencies for this lab
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


### Deployment

Not wired up yet. Upstream lab used Hugging Face Spaces; free Gradio hosting there ended — Render is the free alternative in the course.
