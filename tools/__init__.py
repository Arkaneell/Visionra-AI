from .framework_tool import framework_advisor
from .idea_eval_tool import evaluate_startup_idea
from .knowledge_tool import query_knowledge_base

# Master tool registry — add new tools here as modules grow
ALL_TOOLS = [
    framework_advisor,
    evaluate_startup_idea,
    query_knowledge_base,
]

__all__ = [
    "framework_advisor",
    "evaluate_startup_idea",
    "query_knowledge_base",
    "ALL_TOOLS",
]
