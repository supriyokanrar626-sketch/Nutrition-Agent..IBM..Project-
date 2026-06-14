"""
Agent 1: Nutrition Knowledge Agent
Retrieves and summarizes nutritional data using RAG + IBM Granite.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from rag.knowledge_base import get_knowledge_base
from agents.llm_helper import call_granite, build_prompt

SYSTEM_PROMPT = """You are the Nutrition Knowledge Agent, powered by IBM Granite AI.
Your role is to provide accurate, science-backed nutritional information.
You have access to a knowledge base of nutritional data including:
- Macronutrients and micronutrients
- Calorie content of foods
- Vitamins and minerals
- Indian and international foods

Always provide:
1. Specific nutritional values (calories, protein, carbs, fat)
2. Key vitamins and minerals
3. Health benefits
4. Practical tips

Be concise, accurate, and helpful. Use bullet points for clarity."""


def run(query: str) -> str:
    """
    Main entry point for Nutrition Knowledge Agent.
    
    Args:
        query: User's nutrition question
    Returns:
        Detailed nutritional information
    """
    kb = get_knowledge_base()
    context = kb.get_context(query, top_k=4)

    prompt = build_prompt(
        system=SYSTEM_PROMPT,
        user=query,
        context=context
    )

    response = call_granite(prompt, max_tokens=600)
    return response


if __name__ == "__main__":
    result = run("What are the nutritional values of dal and rice?")
    print(result)
