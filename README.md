# Entrepreneurship & Innovation Intelligence Agent

A modular AI agent system for founders, innovators, and startup teams.  
Built with **LangChain + LangGraph + Groq**.

---

## Architecture

```
main.py                         ← CLI entrypoint
agent/agent.py                  ← LangGraph StateGraph orchestrator
tools/
  framework_tool.py             ← Strategy framework advisor (lean canvas, SWOT, etc.)
  idea_eval_tool.py             ← Startup idea evaluator & scorer
  knowledge_tool.py             ← Curated entrepreneurship knowledge base
prompts/
  framework.py                  ← Prompt templates for framework tool
  idea_eval.py                  ← Prompt templates for idea evaluation
  knowledge.py                  ← Prompt templates for knowledge retrieval
llm/
  groq_client.py                ← Groq LLM wrapper
config/
  settings.py                   ← Environment config & model settings
memory/
  session.py                    ← In-session conversation state
utils/
  helpers.py                    ← Shared utility functions
tests/                          ← Unit tests per module
data/                           ← Static KB files, sample startup ideas
```

---

## Quickstart

### 1. Clone & install
```bash
git clone https://github.com/your-org/entrepreneurship-agent.git
cd entrepreneurship-agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 3. Run
```bash
python main.py
```

---

## Adding a New Module

1. Create `tools/your_tool.py` — implement a function decorated with `@tool`
2. Create `prompts/your_tool.py` — define system and user prompt templates
3. Register the tool in `agent/agent.py` → `TOOLS` list
4. Add tests in `tests/test_your_tool.py`

That's it — the LangGraph agent auto-binds all registered tools.

---

## Tech Stack

| Layer | Library |
|---|---|
| LLM | `groq` (llama3-70b-8192) |
| Agent / Graph | `langgraph` |
| Tools / Chains | `langchain` |
| Config | `pydantic-settings` |
| Testing | `pytest` |

---

## Roadmap

- [ ] Framework Advisory Tool (lean canvas, SWOT, Porter's Five Forces)
- [ ] Startup Idea Evaluator (market size, problem clarity, uniqueness score)
- [ ] Entrepreneurship Knowledge Base (curated patterns, case studies)
- [ ] Pitch Deck Outline Generator
- [ ] Competitor Analysis Tool
- [ ] Milestone Planner
- [ ] Web UI (Streamlit / FastAPI)
