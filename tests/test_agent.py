"""
Unit tests for the agent orchestrator.
"""

from unittest.mock import MagicMock, patch
import pytest


class TestEntrepreneurshipAgent:
    @patch("agent.agent.get_llm")
    def test_chat_returns_string(self, mock_get_llm):
        mock_llm = MagicMock()
        # Simulate a direct response (no tool calls)
        mock_response = MagicMock()
        mock_response.tool_calls = []
        mock_response.content = "Hello! I'm your entrepreneurship agent."
        mock_llm.bind_tools.return_value.invoke.return_value = mock_response
        mock_get_llm.return_value = mock_llm

        from agent.agent import EntrepreneurshipAgent
        agent = EntrepreneurshipAgent()
        result = agent.chat("Hi, what can you do?")

        assert isinstance(result, str)
        assert len(result) > 0

    @patch("agent.agent.get_llm")
    def test_reset_clears_memory(self, mock_get_llm):
        mock_get_llm.return_value = MagicMock()

        from agent.agent import EntrepreneurshipAgent
        agent = EntrepreneurshipAgent()
        agent.memory.add_user("test message")

        assert len(agent.memory.get_messages()) == 1
        agent.reset()
        assert len(agent.memory.get_messages()) == 0


class TestSessionMemory:
    def test_add_and_retrieve(self):
        from memory.session import SessionMemory
        mem = SessionMemory(limit=10)
        mem.add_user("Hello")
        mem.add_ai("Hi there!")
        messages = mem.get_messages()
        assert len(messages) == 2

    def test_sliding_window(self):
        from memory.session import SessionMemory
        mem = SessionMemory(limit=4)
        for i in range(6):
            mem.add_user(f"msg {i}")
        assert len(mem.get_messages()) == 4

    def test_clear(self):
        from memory.session import SessionMemory
        mem = SessionMemory()
        mem.add_user("something")
        mem.clear()
        assert len(mem.get_messages()) == 0
