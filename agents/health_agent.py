"""
Agent 3: Health Advisory Agent
Provides preventive health suggestions and disease-specific diet advice.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from rag.knowledge_base import get_knowledge_base
from agents.llm_helper import call_granite, build_prompt

SYSTEM_PROMPT = """You are the Health Advisory Agent, powered by IBM Granite AI.
You are an expert in preventive nutrition and disease-specific dietary management.

You specialize in:
- Diabetes management through diet (Type 1 & Type 2)
- Cardiovascular health and heart-healthy diets
- Hypertension (high blood pressure) management
- Weight management and obesity prevention
- Gut health and digestive disorders
- PCOS/thyroid management through nutrition
- Bone health (osteoporosis prevention)
- Anemia and iron deficiency
- Kidney disease dietary management
- Pregnancy and lactation nutrition
- Sports and athletic nutrition

Always provide:
1. Evidence-based recommendations
2. Foods to eat and foods to avoid
3. Specific nutrients to focus on
4. Lifestyle tips alongside diet advice
5. When to consult a healthcare provider

Important: Always remind users to consult their doctor for medical decisions."""


def run(health_concern: str, user_profile: dict = None) -> str:
    """
    Provide health advisory based on condition.
    
    Args:
        health_concern: The health condition or concern
        user_profile: Optional user profile dict
    Returns:
        Health advisory with dietary recommendations
    """
    kb = get_knowledge_base()
    context = kb.get_context(health_concern, top_k=5)

    profile_info = ""
    if user_profile:
        profile_info = f"\nUser Profile: Age {user_profile.get('age', 'N/A')}, "
        profile_info += f"Gender: {user_profile.get('gender', 'N/A')}, "
        profile_info += f"Conditions: {user_profile.get('conditions', 'None')}"

    user_message = f"""Provide comprehensive health advisory for: {health_concern}
{profile_info}

Include:
1. Overview of how diet affects this condition
2. Top 10 foods to eat (with reasons)
3. Foods/ingredients to strictly avoid
4. Sample meal timing and structure
5. Key nutrients and their daily targets
6. Lifestyle recommendations
7. Warning signs to watch for
8. When to consult a doctor"""

    prompt = build_prompt(
        system=SYSTEM_PROMPT,
        user=user_message,
        context=context
    )

    return call_granite(prompt, max_tokens=900)


HEALTH_CONDITIONS = [
    "Type 2 Diabetes",
    "Hypertension (High Blood Pressure)",
    "High Cholesterol",
    "Heart Disease",
    "Obesity / Weight Management",
    "PCOS (Polycystic Ovary Syndrome)",
    "Thyroid Disorders",
    "Anemia / Iron Deficiency",
    "Osteoporosis / Bone Health",
    "Kidney Disease (CKD)",
    "IBS / Digestive Issues",
    "Pregnancy Nutrition",
    "General Wellness"
]

if __name__ == "__main__":
    result = run("Type 2 Diabetes management through diet")
    print(result)
