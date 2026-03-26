"""
Core agent orchestrator using LangGraph StateGraph.

Flow:
  user input → route_input → [tool_node | direct_llm] → format_output → END

Adding a new tool:
  1. Create tools/your_tool.py with a @tool decorated function
  2. Import and add it to tools/__init__.py → ALL_TOOLS
  That's all — the agent auto-binds via llm.bind_tools(ALL_TOOLS).
"""

from typing import Annotated, TypedDict, Literal
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from llm import get_llm
from tools import ALL_TOOLS
from memory import SessionMemory
from config import settings


# ── State schema ──────────────────────────────────────────────────────────────

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ── System prompt ─────────────────────────────────────────────────────────────

AGENT_SYSTEM_PROMPT = """You are the Entrepreneurship & Innovation Intelligence Agent —
a high-performance AI advisor for founders and startup teams.

You have access to three specialist tools:

1. framework_advisor       — Apply strategy frameworks (Lean Canvas, SWOT, BMC, etc.)
2. evaluate_startup_idea   — Score and critique startup ideas across 7 dimensions
3. query_knowledge_base    — Answer entrepreneurship questions with curated insights

Decision rules:
- If the founder asks to fill out or apply a framework → use framework_advisor
- If the founder describes a startup idea and wants feedback → use evaluate_startup_idea
- If the founder asks a general startup / business question → use query_knowledge_base
- For greetings or meta questions about you → answer directly without a tool

Always be specific, structured, and founder-centric. Avoid generic advice."""


# ── Node: call the LLM (with tools bound) ─────────────────────────────────────

def call_model(state: AgentState, config: RunnableConfig) -> AgentState:
    llm = get_llm()
    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    messages = [SystemMessage(content=AGENT_SYSTEM_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages, config)
    return {"messages": [response]}


# ── Edge: decide whether to call a tool or finish ─────────────────────────────

def should_continue(state: AgentState) -> Literal["tools", "end"]:
    last = state["messages"][-1]
    if isinstance(last, AIMessage) and last.tool_calls:
        return "tools"
    return "end"


# ── Graph assembly ────────────────────────────────────────────────────────────

def build_graph() -> StateGraph:
    tool_node = ToolNode(ALL_TOOLS)

    graph = StateGraph(AgentState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", tool_node)

    graph.set_entry_point("agent")

    graph.add_conditional_edges(
        "agent",
        should_continue,
        {"tools": "tools", "end": END},
    )
    # After tools execute, always go back to the agent for a final response
    graph.add_edge("tools", "agent")

    return graph.compile()


# ── Public interface ──────────────────────────────────────────────────────────

class EntrepreneurshipAgent:
    """
    High-level wrapper around the compiled LangGraph.

    Usage:
        agent = EntrepreneurshipAgent()
        response = agent.chat("Evaluate my idea: an AI-powered pitch coach")
    """

    def __init__(self):
        self.graph = build_graph()
        self.memory = SessionMemory()

    def chat(self, user_input: str) -> str:
        self.memory.add_user(user_input)

        result = self.graph.invoke(
            {"messages": self.memory.get_messages()},
            config={"recursion_limit": settings.agent_max_iterations},
        )

        # Last message in the result is the final AI response
        final_message = result["messages"][-1]
        content = final_message.content

        self.memory.add_ai(content)
        return content

    def reset(self) -> None:
        """Clear conversation history."""
        self.memory.clear()
