"""
Entrepreneurship Knowledge Base Tool.

Answers founder questions using curated startup knowledge,
frameworks, and real-world patterns.
"""

from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from llm import get_llm
from prompts import KNOWLEDGE_SYSTEM_PROMPT, build_knowledge_prompt


@tool
def query_knowledge_base(question: str) -> str:
    """
    Answer entrepreneurship questions using curated startup knowledge.

    Covers: fundraising, pricing, go-to-market, hiring, pivoting,
    co-founder dynamics, pitch storytelling, and more.

    Args:
        question: The founder's question about startups or entrepreneurship.

    Returns:
        Structured, opinionated answer with frameworks, examples, and citations.
    """
    llm = get_llm()
    messages = [
        SystemMessage(content=KNOWLEDGE_SYSTEM_PROMPT),
        HumanMessage(content=build_knowledge_prompt(question)),
    ]
    response = llm.invoke(messages)
    return response.content
