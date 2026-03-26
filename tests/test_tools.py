"""
Unit tests for all three tools.

These tests mock the LLM to avoid real API calls during CI.
Run: pytest tests/ -v
"""

from unittest.mock import MagicMock, patch
import pytest


# ── Framework Tool ────────────────────────────────────────────────────────────

class TestFrameworkAdvisor:
    @patch("tools.framework_tool.get_llm")
    def test_lean_canvas_returns_content(self, mock_get_llm):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(content="## Lean Canvas\n...")
        mock_get_llm.return_value = mock_llm

        from tools.framework_tool import framework_advisor
        result = framework_advisor.invoke({
            "framework_name": "Lean Canvas",
            "startup_context": "B2B SaaS for remote team async standups",
        })

        assert "Lean Canvas" in result or len(result) > 0
        mock_llm.invoke.assert_called_once()

    @patch("tools.framework_tool.get_llm")
    def test_unsupported_framework_returns_error(self, mock_get_llm):
        from tools.framework_tool import framework_advisor
        result = framework_advisor.invoke({
            "framework_name": "Unknown Framework XYZ",
            "startup_context": "some context",
        })
        assert "not yet supported" in result.lower() or "Available" in result


# ── Idea Evaluation Tool ──────────────────────────────────────────────────────

class TestIdeaEvaluator:
    @patch("tools.idea_eval_tool.get_llm")
    def test_evaluation_returns_content(self, mock_get_llm):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(
            content="## Evaluation\nScore: 7/10\n..."
        )
        mock_get_llm.return_value = mock_llm

        from tools.idea_eval_tool import evaluate_startup_idea
        result = evaluate_startup_idea.invoke({
            "idea_description": "An AI co-pilot for solo founders",
            "additional_context": "Early stage, no traction yet",
        })

        assert len(result) > 0
        mock_llm.invoke.assert_called_once()

    @patch("tools.idea_eval_tool.get_llm")
    def test_evaluation_without_context(self, mock_get_llm):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(content="Evaluation result")
        mock_get_llm.return_value = mock_llm

        from tools.idea_eval_tool import evaluate_startup_idea
        result = evaluate_startup_idea.invoke({
            "idea_description": "Marketplace for freelance CFOs",
        })
        assert len(result) > 0


# ── Knowledge Base Tool ───────────────────────────────────────────────────────

class TestKnowledgeBase:
    @patch("tools.knowledge_tool.get_llm")
    def test_knowledge_query_returns_content(self, mock_get_llm):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = MagicMock(
            content="Product-led growth means the product itself drives acquisition..."
        )
        mock_get_llm.return_value = mock_llm

        from tools.knowledge_tool import query_knowledge_base
        result = query_knowledge_base.invoke({
            "question": "What is product-led growth and when should I use it?"
        })

        assert len(result) > 0
        mock_llm.invoke.assert_called_once()
