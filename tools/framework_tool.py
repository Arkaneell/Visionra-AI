"""
Framework Advisory Tool.

Guides founders through structured strategy frameworks.
"""

from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from llm import get_llm
from prompts import FRAMEWORK_SYSTEM_PROMPT, build_framework_prompt


SUPPORTED_FRAMEWORKS = [
    "Lean Canvas",
    "SWOT Analysis",
    "Porter's Five Forces",
    "Business Model Canvas",
    "Jobs-to-be-Done",
    "OKR Planning",
    "Value Proposition Canvas",
]


@tool
def framework_advisor(framework_name: str, startup_context: str) -> str:
    """
    Apply a startup strategy framework to the founder's context.

    Args:
        framework_name: Name of the framework (e.g. 'Lean Canvas', 'SWOT Analysis').
        startup_context: Description of the startup — product, market, stage, problem.

    Returns:
        A fully completed framework analysis with actionable insights.
    """
    if framework_name not in SUPPORTED_FRAMEWORKS:
        closest = next(
            (f for f in SUPPORTED_FRAMEWORKS if framework_name.lower() in f.lower()),
            None,
        )
        if closest:
            framework_name = closest
        else:
            return (
                f"Framework '{framework_name}' is not yet supported.\n"
                f"Available: {', '.join(SUPPORTED_FRAMEWORKS)}"
            )

    llm = get_llm()
    messages = [
        SystemMessage(content=FRAMEWORK_SYSTEM_PROMPT),
        HumanMessage(content=build_framework_prompt(framework_name, startup_context)),
    ]
    response = llm.invoke(messages)
    return response.content
