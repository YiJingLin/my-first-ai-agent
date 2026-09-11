# Profile Chatbot
This first project is to create a profile/career chatbot. 
1. The chatbot will use OpenAI API as LLM backend. 
2. During conversation, the LLM will decide whether call the tooling function we define. 
3. Lastly, we are able to deploy the chatbot to Hugging face as cloud service.

ref: https://github.com/ed-donner/agents/blob/main/1_foundations/4_lab4.ipynb

Policy harness / live gate: see `../2_harness/`.

## Prerequisites

- Parent `.env` with `OPENAI_API_KEY`
- `pip install -r requirements.txt` then open/run the notebook

## Project Structure

```
1_profile_chatbot/
  profile_chatbot.ipynb   # OpenAI + tools + Gradio
  summary.txt             # short bio fed into the system prompt
  linkedin.pdf            # optional LinkedIn PDF for extra context
  requirements.txt
```

### Lab in Jupyter Notebook

`profile_chatbot.ipynb` — chat loop with tool calling.

### Run Python Script

Not yet — logic lives in the notebook for now.

### Deployment

Not wired up yet. Upstream lab used Hugging Face Spaces; free Gradio hosting there ended — Render is the free alternative in the course.
