"""
In-session conversation memory.

Wraps LangChain's ConversationBufferWindowMemory with a configurable window
and exposes simple get/set helpers for use in the LangGraph state.
"""

from typing import List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from config import settings


class SessionMemory:
    """Simple sliding-window message store for one agent session."""

    def __init__(self, limit: int | None = None):
        self._limit = limit or settings.session_history_limit
        self._messages: List[BaseMessage] = []

    def add_user(self, text: str) -> None:
        self._messages.append(HumanMessage(content=text))
        self._trim()

    def add_ai(self, text: str) -> None:
        self._messages.append(AIMessage(content=text))
        self._trim()

    def get_messages(self) -> List[BaseMessage]:
        return list(self._messages)

    def clear(self) -> None:
        self._messages = []

    def _trim(self) -> None:
        if len(self._messages) > self._limit:
            # Keep the most recent messages
            self._messages = self._messages[-self._limit :]
