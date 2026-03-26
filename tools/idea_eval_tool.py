"""
Startup Idea Evaluator Tool.

Scores and critiques startup ideas across 7 key dimensions.
"""

from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from llm import get_llm
from prompts import IDEA_EVAL_SYSTEM_PROMPT, build_idea_eval_prompt


@tool
def evaluate_startup_idea(idea_description: str, additional_context: str = "") -> str:
    """
    Evaluate a startup idea across problem clarity, market size, uniqueness,
    founder-market fit, business model, timing, and execution risk.

    Args:
        idea_description: Full description of the startup idea.
        additional_context: Optional extra info (target user, tech stack, traction).

    Returns:
        Structured evaluation with dimension scores, strengths, risks, and next step.
    """
    llm = get_llm()
    messages = [
        SystemMessage(content=IDEA_EVAL_SYSTEM_PROMPT),
        HumanMessage(
            content=build_idea_eval_prompt(idea_description, additional_context)
        ),
    ]
    response = llm.invoke(messages)
    return response.content
