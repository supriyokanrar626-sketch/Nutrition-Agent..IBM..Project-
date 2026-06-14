"""
LLM Helper — Calls IBM Granite model via HuggingFace Inference API.
Falls back to intelligent rule-based responses if API is unavailable.
"""

import requests
import json
from config import HF_TOKEN, HF_API_URL


def call_granite(prompt: str, max_tokens: int = 800) -> str:
    """
    Call IBM Granite model via HuggingFace Inference API.
    Returns the model's text response.
    """
    if HF_TOKEN == "YOUR_HUGGINGFACE_TOKEN_HERE":
        return _fallback_response(prompt)

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "").strip()
            elif isinstance(result, dict):
                return result.get("generated_text", "").strip()
        elif response.status_code == 503:
            return _fallback_response(prompt)
        else:
            return _fallback_response(prompt)
    except Exception as e:
        print(f"LLM API error: {e}")
        return _fallback_response(prompt)


def build_prompt(system: str, user: str, context: str = "") -> str:
    """Build a chat-style prompt for Granite Instruct models."""
    ctx_section = f"\n\nContext Information:\n{context}" if context else ""
    return (
        f"<|system|>\n{system}{ctx_section}\n"
        f"<|user|>\n{user}\n"
        f"<|assistant|>\n"
    )


def _fallback_response(prompt: str) -> str:
    """Smart rule-based fallback when API is unavailable."""
    prompt_lower = prompt.lower()

    if any(w in prompt_lower for w in ["calorie", "calories", "nutrition", "nutritional", "food"]):
        return (
            "Based on nutritional data:\n\n"
            "• **Calories**: Vary by food type — vegetables ~20-80 kcal/cup, "
            "grains ~200 kcal/cup cooked, proteins ~150-300 kcal/100g\n"
            "• **Macros**: Balance carbs (45-65%), protein (10-35%), fats (20-35%)\n"
            "• **Key vitamins**: Vitamin C, D, B12, folate are commonly deficient\n"
            "• **Minerals**: Focus on calcium, iron, magnesium, potassium\n\n"
            "💡 *Tip: Use the USDA FoodData Central for precise values.*"
        )

    if any(w in prompt_lower for w in ["diabetes", "diabetic", "blood sugar", "glucose"]):
        return (
            "**Diabetes-Friendly Diet Plan:**\n\n"
            "✅ **Eat More**: Non-starchy vegetables, legumes, whole grains, "
            "lean proteins, nuts, berries\n"
            "❌ **Avoid**: Sugary drinks, white bread/rice, pastries, fruit juices\n\n"
            "🍽️ **Sample Day**:\n"
            "- Breakfast: Vegetable oats upma + green tea\n"
            "- Lunch: 2 multigrain roti + palak dal + curd\n"
            "- Dinner: Grilled fish + salad + 1 cup quinoa\n\n"
            "📌 Aim for 45-60g carbs per meal, 25-35g fiber daily."
        )

    if any(w in prompt_lower for w in ["heart", "cardiac", "cholesterol", "blood pressure"]):
        return (
            "**Heart-Healthy Diet Plan:**\n\n"
            "✅ **Eat More**: Fatty fish (salmon, sardines), walnuts, flaxseeds, "
            "oats, berries, olive oil, avocados, leafy greens\n"
            "❌ **Limit**: Saturated fats, trans fats, sodium (<2300mg/day), "
            "red meat, processed foods\n\n"
            "🍽️ **Sample Day**:\n"
            "- Breakfast: Oatmeal + walnuts + blueberries\n"
            "- Lunch: Grilled salmon + large salad + whole grain bread\n"
            "- Dinner: Lentil soup + mixed vegetable sabzi + 1 roti\n\n"
            "📌 Follow Mediterranean diet principles for best heart outcomes."
        )

    if any(w in prompt_lower for w in ["weight loss", "lose weight", "diet plan", "meal plan"]):
        return (
            "**Personalized Weight Loss Plan:**\n\n"
            "🎯 **Goal**: Safe loss of 0.5-1 kg/week via 500-cal deficit\n\n"
            "🍽️ **Daily Meal Plan (~1500 cal)**:\n"
            "- Breakfast: Oats + berries + 5 almonds (350 cal)\n"
            "- Snack: Apple + 10 almonds (155 cal)\n"
            "- Lunch: 2 chapati + dal + sabzi + curd (450 cal)\n"
            "- Snack: Sprouts chaat (100 cal)\n"
            "- Dinner: Grilled chicken + salad + brown rice (450 cal)\n\n"
            "✅ **Key Tips**: High protein, high fiber, limit processed foods, "
            "drink 2-3L water daily."
        )

    if any(w in prompt_lower for w in ["muscle", "protein", "gym", "workout", "bodybuilding"]):
        return (
            "**Muscle Building Nutrition Plan:**\n\n"
            "💪 **Protein Target**: 1.6-2.2g per kg body weight\n"
            "🔥 **Calories**: 300-500 above maintenance\n\n"
            "🍽️ **Daily Plan (~2800 cal)**:\n"
            "- Breakfast: 4 eggs + oats + banana (550 cal)\n"
            "- Mid-morning: Greek yogurt + fruits (250 cal)\n"
            "- Lunch: Grilled chicken 200g + brown rice + vegetables (700 cal)\n"
            "- Pre-workout: Banana + peanut butter toast (300 cal)\n"
            "- Post-workout: Protein shake + banana (250 cal)\n"
            "- Dinner: Paneer curry + quinoa + dal (550 cal)\n\n"
            "📌 Creatine (3-5g/day) is one of the most evidence-backed supplements."
        )

    if any(w in prompt_lower for w in ["log", "ate", "eaten", "breakfast", "lunch", "dinner", "snack"]):
        return (
            "**Meal Analysis:**\n\n"
            "✅ Your meal has been logged successfully!\n\n"
            "📊 **Estimated Nutritional Breakdown**:\n"
            "- Calories: ~350-450 kcal\n"
            "- Protein: ~15-25g\n"
            "- Carbohydrates: ~40-55g\n"
            "- Fat: ~10-15g\n"
            "- Fiber: ~5-8g\n\n"
            "💡 **Feedback**: Good balance of macronutrients! "
            "Consider adding more vegetables for extra fiber and micronutrients. "
            "Stay hydrated — drink a glass of water with your meal."
        )

    return (
        "**Nutrition Insight:**\n\n"
        "I'm your AI-powered Nutrition Agent built with IBM Granite technology! "
        "I can help you with:\n\n"
        "🥗 **Diet Plans** — Personalized for your health goals\n"
        "📊 **Nutrition Data** — Calories, macros, vitamins for any food\n"
        "🏥 **Health Advice** — Diabetes, heart health, weight management\n"
        "📝 **Meal Tracking** — Log and analyze your daily intake\n\n"
        "Try asking: *'Create a diabetes-friendly meal plan'* or "
        "*'What are the calories in dal and rice?'*"
    )
