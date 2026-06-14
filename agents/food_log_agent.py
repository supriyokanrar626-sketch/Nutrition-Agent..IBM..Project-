"""
Agent 4: Food Log & Feedback Agent
Tracks meals, analyzes nutrition, and provides actionable feedback.
"""

import sys, os, json
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from agents.llm_helper import call_granite, build_prompt

SYSTEM_PROMPT = """You are the Food Log & Feedback Agent, powered by IBM Granite AI.
You analyze logged meals and provide instant nutritional feedback.

When analyzing a meal log:
1. Estimate total calories and macros (protein, carbs, fat, fiber)
2. Identify key vitamins and minerals present
3. Highlight nutritional strengths of the meal
4. Point out any nutritional gaps or concerns
5. Suggest simple improvements
6. Give an overall nutrition score (1-10)
7. Provide hydration reminders

Be encouraging, practical, and specific. Use emojis for visual appeal."""

# --- In-memory meal log (session-based) ---
meal_log = []


def log_meal(meal_description: str, meal_type: str = "Meal") -> dict:
    """
    Log a meal and analyze its nutrition.
    
    Args:
        meal_description: Text description of the meal
        meal_type: Breakfast/Lunch/Dinner/Snack
    Returns:
        Dict with meal entry and AI analysis
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    user_message = f"""Analyze this {meal_type} and provide nutritional feedback:

Meal: {meal_description}

Provide:
1. Estimated calories (give a specific range)
2. Macronutrient breakdown (protein, carbs, fat in grams)
3. Key vitamins and minerals in this meal
4. Nutritional strengths (what's good about this meal)
5. Areas to improve
6. One simple swap to make it healthier
7. Overall nutrition score out of 10"""

    prompt = build_prompt(system=SYSTEM_PROMPT, user=user_message)
    analysis = call_granite(prompt, max_tokens=700)

    entry = {
        "timestamp": timestamp,
        "meal_type": meal_type,
        "description": meal_description,
        "analysis": analysis,
        "estimated_nutrition": _estimate_nutrition(meal_description)
    }

    meal_log.append(entry)
    return entry


def get_daily_summary() -> str:
    """Generate a comprehensive daily nutrition summary."""
    if not meal_log:
        return "No meals logged yet today. Start logging your meals to track your nutrition! 📝"

    meals_text = "\n".join([
        f"- {m['meal_type']} ({m['timestamp'].split()[1]}): {m['description']}"
        for m in meal_log
    ])

    # Calculate totals
    totals = _calculate_daily_totals()

    user_message = f"""Provide a daily nutrition summary for these logged meals:

{meals_text}

Estimated Daily Totals:
- Total Calories: ~{totals['calories']} kcal
- Protein: ~{totals['protein']}g
- Carbohydrates: ~{totals['carbs']}g
- Fat: ~{totals['fat']}g
- Fiber: ~{totals['fiber']}g

Please provide:
1. Overall nutrition assessment
2. Nutrients meeting daily goals (vs recommended)
3. Nutritional deficiencies today
4. Progress toward typical daily goals
5. Tomorrow's improvement suggestions
6. Hydration check"""

    prompt = build_prompt(system=SYSTEM_PROMPT, user=user_message)
    return call_granite(prompt, max_tokens=700)


def get_weekly_report(weekly_logs: list) -> str:
    """Generate a weekly nutrition report."""
    summary = f"Weekly analysis of {len(weekly_logs)} logged meal days."
    user_message = f"""{summary}
Provide:
1. Weekly calorie average
2. Most/least nutritious days
3. Recurring nutritional patterns
4. Key deficiencies to address
5. Weekly progress assessment
6. Goals for next week"""
    prompt = build_prompt(system=SYSTEM_PROMPT, user=user_message)
    return call_granite(prompt, max_tokens=600)


def _estimate_nutrition(meal: str) -> dict:
    """Rule-based nutrition estimator for common Indian/international foods."""
    meal_lower = meal.lower()
    nutrition = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0}

    food_db = {
        "rice": {"calories": 206, "protein": 4, "carbs": 45, "fat": 0.4, "fiber": 0.6},
        "dal": {"calories": 230, "protein": 18, "carbs": 40, "fat": 1, "fiber": 15},
        "roti": {"calories": 80, "protein": 3, "carbs": 15, "fat": 1, "fiber": 1.5},
        "chapati": {"calories": 80, "protein": 3, "carbs": 15, "fat": 1, "fiber": 1.5},
        "chicken": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "fiber": 0},
        "fish": {"calories": 150, "protein": 22, "carbs": 0, "fat": 7, "fiber": 0},
        "egg": {"calories": 78, "protein": 6, "carbs": 0.6, "fat": 5, "fiber": 0},
        "paneer": {"calories": 265, "protein": 18, "carbs": 3.4, "fat": 20, "fiber": 0},
        "oats": {"calories": 154, "protein": 6, "carbs": 27, "fat": 3, "fiber": 4},
        "milk": {"calories": 149, "protein": 8, "carbs": 12, "fat": 8, "fiber": 0},
        "banana": {"calories": 105, "protein": 1.3, "carbs": 27, "fat": 0.4, "fiber": 3},
        "apple": {"calories": 95, "protein": 0.5, "carbs": 25, "fat": 0.3, "fiber": 4},
        "salad": {"calories": 50, "protein": 2, "carbs": 10, "fat": 0.5, "fiber": 3},
        "bread": {"calories": 70, "protein": 3, "carbs": 13, "fat": 1, "fiber": 1},
        "idli": {"calories": 70, "protein": 2, "carbs": 14, "fat": 0.5, "fiber": 1},
        "dosa": {"calories": 120, "protein": 3, "carbs": 22, "fat": 3, "fiber": 1},
        "samosa": {"calories": 200, "protein": 4, "carbs": 22, "fat": 12, "fiber": 2},
        "biryani": {"calories": 350, "protein": 20, "carbs": 45, "fat": 12, "fiber": 2},
        "curd": {"calories": 100, "protein": 5, "carbs": 8, "fat": 5, "fiber": 0},
        "yogurt": {"calories": 130, "protein": 22, "carbs": 9, "fat": 0.7, "fiber": 0},
        "coffee": {"calories": 5, "protein": 0.3, "carbs": 1, "fat": 0.1, "fiber": 0},
        "tea": {"calories": 2, "protein": 0, "carbs": 0.5, "fat": 0, "fiber": 0},
    }

    matched = False
    for food, vals in food_db.items():
        if food in meal_lower:
            # Estimate portions (rough)
            multiplier = 1
            if any(w in meal_lower for w in ["2", "two", "double"]):
                multiplier = 2
            elif any(w in meal_lower for w in ["half", "small"]):
                multiplier = 0.5
            for key in nutrition:
                nutrition[key] += vals[key] * multiplier
            matched = True

    if not matched:
        # Generic estimate
        nutrition = {"calories": 350, "protein": 15, "carbs": 40, "fat": 10, "fiber": 5}

    return {k: round(v) for k, v in nutrition.items()}


def _calculate_daily_totals() -> dict:
    """Sum up estimated nutrition from all logged meals."""
    totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0}
    for entry in meal_log:
        n = entry.get("estimated_nutrition", {})
        for key in totals:
            totals[key] += n.get(key, 0)
    return totals


def get_meal_log() -> list:
    """Return current session meal log."""
    return meal_log


def clear_log():
    """Clear the meal log."""
    meal_log.clear()


if __name__ == "__main__":
    entry = log_meal("2 chapati with dal and mixed vegetable sabzi and curd", "Lunch")
    print(entry["analysis"])
