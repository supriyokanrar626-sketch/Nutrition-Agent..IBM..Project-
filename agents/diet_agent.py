"""
Agent 2: Diet Recommendation Agent
Generates personalized meal plans based on user profile.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from rag.knowledge_base import get_knowledge_base
from agents.llm_helper import call_granite, build_prompt

SYSTEM_PROMPT = """You are the Diet Recommendation Agent, powered by IBM Granite AI.
You create highly personalized meal plans based on individual user profiles.

When generating meal plans, always consider:
- Age, gender, weight, height
- Health conditions (diabetes, hypertension, etc.)
- Dietary preferences (vegetarian, vegan, non-vegetarian)
- Food allergies and intolerances
- Fitness goals (weight loss, muscle gain, maintenance)
- Cultural food preferences (Indian, Mediterranean, etc.)
- Activity level

Structure your meal plans with:
1. Daily calorie target
2. Macro breakdown (carbs/protein/fat)
3. Breakfast, Lunch, Dinner + Snacks
4. Hydration recommendations
5. Key nutritional tips

Make plans practical, delicious, and culturally appropriate."""


def run(user_profile: dict, goal: str = "") -> str:
    """
    Generate personalized diet plan.
    
    Args:
        user_profile: dict with age, weight, height, conditions, preferences, etc.
        goal: specific dietary goal
    Returns:
        Personalized meal plan
    """
    kb = get_knowledge_base()

    # Build profile string
    profile_str = _format_profile(user_profile)
    query = f"{profile_str} Goal: {goal}"
    context = kb.get_context(query, top_k=5)

    user_message = f"""Create a detailed personalized diet plan for this person:

{profile_str}
Goal: {goal if goal else 'Balanced healthy diet'}

Please provide:
1. Daily calorie target
2. Macro targets (protein, carbs, fat in grams)
3. Complete 1-day meal plan with portion sizes
4. Key food recommendations
5. Foods to avoid
6. 3 practical nutrition tips"""

    prompt = build_prompt(
        system=SYSTEM_PROMPT,
        user=user_message,
        context=context
    )

    return call_granite(prompt, max_tokens=900)


def _format_profile(profile: dict) -> str:
    """Convert profile dict to readable string."""
    parts = []
    if profile.get("age"): parts.append(f"Age: {profile['age']} years")
    if profile.get("gender"): parts.append(f"Gender: {profile['gender']}")
    if profile.get("weight"): parts.append(f"Weight: {profile['weight']} kg")
    if profile.get("height"): parts.append(f"Height: {profile['height']} cm")
    if profile.get("activity"): parts.append(f"Activity level: {profile['activity']}")
    if profile.get("conditions"): parts.append(f"Health conditions: {profile['conditions']}")
    if profile.get("diet_type"): parts.append(f"Diet preference: {profile['diet_type']}")
    if profile.get("allergies"): parts.append(f"Allergies: {profile['allergies']}")
    return "\n".join(parts) if parts else "No profile provided"


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor equation."""
    if gender.lower() == "male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161


def calculate_tdee(bmr: float, activity: str) -> float:
    """Calculate Total Daily Energy Expenditure."""
    multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extra Active": 1.9
    }
    return bmr * multipliers.get(activity, 1.375)


if __name__ == "__main__":
    profile = {
        "age": 25, "gender": "Female", "weight": 60, "height": 162,
        "activity": "Moderately Active", "conditions": "None",
        "diet_type": "Vegetarian", "allergies": "None"
    }
    result = run(profile, "Weight loss")
    print(result)
