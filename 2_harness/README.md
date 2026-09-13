# Prompt harness

Career twin with offline evaluation probes and a live policy gate (refuse unrelated / suspicious / dangerous asks).

## Prerequisites

- Parent `.env` with `OPENAI_API_KEY`
- `summary.txt` (and optional `linkedin.pdf`) in this folder
- `pip install -r requirements.txt`

## Project structure

```
2_harness/
  harness.ipynb      # twin + harness + gated Gradio
  summary.txt        # short bio fed into the system prompt
  linkedin.pdf       # optional LinkedIn PDF for extra context
  requirements.txt
```

## What to run

1. Offline: run cells through `run_harness()` to score the raw twin
2. Optional: `run_harness(reply_fn=chat)` to score the gated path
3. Gradio: last cell launches chat with input/output gates
