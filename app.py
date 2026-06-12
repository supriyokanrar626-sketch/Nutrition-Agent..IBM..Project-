"""
NutriAgent AI — IBM-Powered Nutrition Intelligence Platform
Main Streamlit Application
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="NutriAgent AI | IBM Granite",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }

.hero-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    padding: 2.5rem 2rem;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 20px 60px rgba(102,126,234,0.4);
}
.hero-banner h1 { color: white; font-size: 2.8rem; font-weight: 700; margin: 0; letter-spacing: -1px; }
.hero-banner p { color: rgba(255,255,255,0.85); font-size: 1.1rem; margin-top: 0.5rem; }

.agent-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    color: white;
}
.metric-card {
    background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.2));
    border: 1px solid rgba(102,126,234,0.3);
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
    color: white;
}
.metric-card h3 { font-size: 2rem; font-weight: 700; margin: 0; color: #a78bfa; }
.metric-card p { margin: 0; opacity: 0.7; font-size: 0.85rem; }

.response-box {
    background: rgba(255,255,255,0.07);
    border-left: 4px solid #667eea;
    border-radius: 12px;
    padding: 1.5rem;
    color: white;
    margin-top: 1rem;
    line-height: 1.8;
}
.meal-entry {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin: 0.4rem 0;
    color: white;
    border-left: 3px solid #34d399;
}
.sidebar-profile { color: white; }
.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s;
    width: 100%;
}
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(102,126,234,0.5); }
.stSelectbox label, .stTextInput label, .stTextArea label,
.stSlider label, .stRadio label { color: rgba(255,255,255,0.8) !important; }
.stTextArea textarea, .stTextInput input { background: rgba(255,255,255,0.08) !important; color: white !important; border: 1px solid rgba(255,255,255,0.2) !important; border-radius: 10px !important; }
.stSelectbox > div > div { background: rgba(30,27,60,0.9) !important; color: white !important; border: 1px solid rgba(255,255,255,0.2) !important; border-radius: 10px !important; }
h2, h3 { color: white !important; }
.stTabs [data-baseweb="tab"] { color: rgba(255,255,255,0.6) !important; font-weight: 500; }
.stTabs [aria-selected="true"] { color: #a78bfa !important; border-bottom: 2px solid #a78bfa !important; }
.stTabs [data-baseweb="tab-list"] { background: rgba(255,255,255,0.05); border-radius: 12px; padding: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────
if "meal_log" not in st.session_state:
    st.session_state.meal_log = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "daily_nutrition" not in st.session_state:
    st.session_state.daily_nutrition = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0}

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <div style='font-size:3rem;'>🥗</div>
        <h2 style='color: #a78bfa; margin:0;'>NutriAgent AI</h2>
        <p style='color: rgba(255,255,255,0.5); font-size:0.8rem;'>Powered by IBM Granite</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 👤 Your Profile")

    age = st.slider("Age", 10, 90, 25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    weight = st.number_input("Weight (kg)", 30.0, 200.0, 65.0, step=0.5)
    height = st.number_input("Height (cm)", 100.0, 220.0, 165.0, step=0.5)
    activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
    diet_type = st.selectbox("Diet Preference", ["Non-Vegetarian", "Vegetarian", "Vegan", "Eggetarian"])
    conditions = st.multiselect("Health Conditions", [
        "None", "Type 2 Diabetes", "Hypertension", "High Cholesterol",
        "PCOS", "Thyroid", "Anemia", "Kidney Disease", "Heart Disease"
    ], default=["None"])
    allergies = st.text_input("Allergies (if any)", placeholder="e.g., nuts, dairy")

    st.divider()

    # BMR calculation
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    act_map = {"Sedentary": 1.2, "Lightly Active": 1.375, "Moderately Active": 1.55, "Very Active": 1.725}
    tdee = bmr * act_map.get(activity, 1.375)

    st.markdown(f"""
    <div class='metric-card'>
        <h3>{int(tdee)}</h3>
        <p>Daily Calorie Need (TDEE)</p>
    </div>
    <div style='margin-top:0.5rem;'></div>
    <div class='metric-card'>
        <h3>{int(bmr)}</h3>
        <p>Basal Metabolic Rate</p>
    </div>
    """, unsafe_allow_html=True)

    user_profile = {
        "age": age, "gender": gender, "weight": weight, "height": height,
        "activity": activity, "diet_type": diet_type,
        "conditions": ", ".join(conditions), "allergies": allergies or "None",
        "tdee": int(tdee), "bmr": int(bmr)
    }

# ── Hero Banner ───────────────────────────────────────────────
st.markdown("""
<div class='hero-banner'>
    <h1>🥗 NutriAgent AI</h1>
    <p>IBM Granite-Powered Multi-Agent Nutrition Intelligence Platform</p>
    <p style='font-size:0.85rem; opacity:0.7;'>Nutrition Knowledge • Diet Planning • Health Advisory • Meal Tracking</p>
</div>
""", unsafe_allow_html=True)

# ── Top Metrics ───────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
logged_cal = st.session_state.daily_nutrition["calories"]
with c1:
    st.markdown(f"<div class='metric-card'><h3>{logged_cal}</h3><p>Calories Today</p></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-card'><h3>{st.session_state.daily_nutrition['protein']}g</h3><p>Protein</p></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-card'><h3>{st.session_state.daily_nutrition['carbs']}g</h3><p>Carbohydrates</p></div>", unsafe_allow_html=True)
with c4:
    remaining = max(0, int(tdee) - logged_cal)
    st.markdown(f"<div class='metric-card'><h3>{remaining}</h3><p>Calories Remaining</p></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Main Tabs ─────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔬 Nutrition Info", "🍽️ Diet Plan", "🏥 Health Advisory", "📝 Meal Logger", "📊 Dashboard"
])

# ═══════════════════════════════════════════════════
# TAB 1 — NUTRITION KNOWLEDGE AGENT
# ═══════════════════════════════════════════════════
with tab1:
    st.markdown("## 🔬 Nutrition Knowledge Agent")
    st.markdown("<p style='color:rgba(255,255,255,0.6);'>Ask about calories, macros, vitamins, minerals for any food.</p>", unsafe_allow_html=True)

    quick_queries = [
        "Nutritional values of dal and rice",
        "Calories in chicken biryani",
        "Vitamins in spinach and broccoli",
        "How much protein is in paneer?",
        "Best foods rich in iron",
        "Omega-3 fatty acid sources"
    ]
    st.markdown("**💡 Quick Questions:**")
    cols = st.columns(3)
    for i, q in enumerate(quick_queries):
        if cols[i % 3].button(q, key=f"q_{i}"):
            st.session_state["nutrition_query"] = q

    query_input = st.text_area(
        "Or type your question:",
        value=st.session_state.get("nutrition_query", ""),
        placeholder="e.g., What are the calories and protein in 2 chapati with dal?",
        height=100, key="nutrition_input"
    )

    if st.button("🔍 Get Nutrition Info", key="btn_nutrition"):
        if query_input.strip():
            with st.spinner("🤖 IBM Granite is analyzing nutritional data..."):
                from agents.nutrition_agent import run as nutrition_run
                result = nutrition_run(query_input)
            st.markdown(f"<div class='response-box'>{result}</div>", unsafe_allow_html=True)
        else:
            st.warning("Please enter a question.")

# ═══════════════════════════════════════════════════
# TAB 2 — DIET RECOMMENDATION AGENT
# ═══════════════════════════════════════════════════
with tab2:
    st.markdown("## 🍽️ Diet Recommendation Agent")
    st.markdown("<p style='color:rgba(255,255,255,0.6);'>Get a personalized meal plan based on your profile.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        goal = st.selectbox("🎯 Your Goal", [
            "Weight Loss", "Muscle Building", "Maintenance",
            "Diabetes Management", "Heart Health", "General Wellness"
        ])
        special_req = st.text_input("Special requirements", placeholder="e.g., no onion garlic, high protein")

    with col2:
        plan_duration = st.radio("Plan Duration", ["1 Day", "3 Days", "7 Days"])
        meal_count = st.selectbox("Meals per day", ["3 meals", "3 meals + 2 snacks", "5-6 small meals"])

    st.markdown("**📋 Your Profile Summary:**")
    st.markdown(f"""
    <div class='agent-card'>
        <b>Age:</b> {age} | <b>Weight:</b> {weight}kg | <b>Height:</b> {height}cm |
        <b>Activity:</b> {activity} | <b>Diet:</b> {diet_type} | <b>Conditions:</b> {', '.join(conditions)}
        <br><b>Daily Calorie Need:</b> {int(tdee)} kcal
    </div>
    """, unsafe_allow_html=True)

    if st.button("🍽️ Generate My Diet Plan", key="btn_diet"):
        with st.spinner("🤖 Creating your personalized diet plan..."):
            from agents.diet_agent import run as diet_run
            full_goal = f"{goal} | {plan_duration} | {meal_count} | {special_req}"
            result = diet_run(user_profile, full_goal)
        st.markdown(f"<div class='response-box'>{result}</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# TAB 3 — HEALTH ADVISORY AGENT
# ═══════════════════════════════════════════════════
with tab3:
    st.markdown("## 🏥 Health Advisory Agent")
    st.markdown("<p style='color:rgba(255,255,255,0.6);'>Disease-specific nutrition guidance and preventive health advice.</p>", unsafe_allow_html=True)

    from agents.health_agent import HEALTH_CONDITIONS
    selected_condition = st.selectbox("Select Health Concern", HEALTH_CONDITIONS)
    custom_concern = st.text_input("Or describe your specific concern:", placeholder="e.g., managing cholesterol after 50")

    col1, col2 = st.columns(2)
    with col1:
        include_profile = st.checkbox("Include my profile in analysis", value=True)
    with col2:
        severity = st.selectbox("Severity", ["Mild", "Moderate", "Severe / Medical"])

    if st.button("🏥 Get Health Advisory", key="btn_health"):
        concern = custom_concern if custom_concern.strip() else selected_condition
        with st.spinner("🤖 Analyzing health data with IBM Granite..."):
            from agents.health_agent import run as health_run
            profile_arg = user_profile if include_profile else None
            result = health_run(f"{concern} (severity: {severity})", profile_arg)
        st.markdown(f"<div class='response-box'>{result}</div>", unsafe_allow_html=True)

        st.info("⚠️ This is AI-generated guidance for educational purposes. Always consult your doctor for medical decisions.")

# ═══════════════════════════════════════════════════
# TAB 4 — FOOD LOG & FEEDBACK AGENT
# ═══════════════════════════════════════════════════
with tab4:
    st.markdown("## 📝 Food Log & Feedback Agent")
    st.markdown("<p style='color:rgba(255,255,255,0.6);'>Log your meals and get instant nutritional analysis.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        meal_desc = st.text_area(
            "What did you eat?",
            placeholder="e.g., 2 chapati with dal, mixed vegetable sabzi and a cup of curd",
            height=100
        )
    with col2:
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Morning Snack", "Evening Snack"])
        log_time = st.text_input("Time (optional)", placeholder="e.g., 8:30 AM")

    if st.button("📝 Log & Analyze Meal", key="btn_log"):
        if meal_desc.strip():
            with st.spinner("🤖 Analyzing your meal..."):
                from agents.food_log_agent import log_meal, _estimate_nutrition
                entry = log_meal(meal_desc, meal_type)
                est = entry["estimated_nutrition"]
                # Update session totals
                for k in st.session_state.daily_nutrition:
                    st.session_state.daily_nutrition[k] += est.get(k, 0)
                st.session_state.meal_log.append(entry)

            st.success(f"✅ {meal_type} logged at {datetime.now().strftime('%I:%M %p')}")
            st.markdown(f"<div class='response-box'>{entry['analysis']}</div>", unsafe_allow_html=True)

            # Show quick nutrition estimate
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Calories", f"~{est['calories']} kcal")
            c2.metric("Protein", f"~{est['protein']}g")
            c3.metric("Carbs", f"~{est['carbs']}g")
            c4.metric("Fat", f"~{est['fat']}g")
        else:
            st.warning("Please describe your meal.")

    # Show meal log
    if st.session_state.meal_log:
        st.markdown("### 📋 Today's Meal Log")
        for entry in st.session_state.meal_log:
            st.markdown(f"""
            <div class='meal-entry'>
                <b>🍽️ {entry['meal_type']}</b> — {entry['description'][:80]}...
                <span style='float:right; opacity:0.6; font-size:0.8rem;'>{entry['timestamp']}</span>
            </div>
            """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Get Daily Summary", key="btn_summary"):
                with st.spinner("Generating daily summary..."):
                    from agents.food_log_agent import get_daily_summary
                    summary = get_daily_summary()
                st.markdown(f"<div class='response-box'>{summary}</div>", unsafe_allow_html=True)
        with col2:
            if st.button("🗑️ Clear Today's Log", key="btn_clear"):
                st.session_state.meal_log = []
                st.session_state.daily_nutrition = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0}
                st.rerun()

# ═══════════════════════════════════════════════════
# TAB 5 — VISUALIZATION DASHBOARD
# ═══════════════════════════════════════════════════
with tab5:
    st.markdown("## 📊 Nutrition Dashboard")

    dn = st.session_state.daily_nutrition
    target_cal = int(tdee)
    target_protein = int(weight * 1.6)
    target_carbs = int((target_cal * 0.50) / 4)
    target_fat = int((target_cal * 0.25) / 9)

    col1, col2 = st.columns(2)

    # Calorie Progress Gauge
    with col1:
        cal_pct = min(100, int((dn["calories"] / target_cal) * 100)) if target_cal > 0 else 0
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=dn["calories"],
            delta={"reference": target_cal},
            title={"text": "Calories Consumed", "font": {"color": "white"}},
            gauge={
                "axis": {"range": [0, target_cal * 1.3], "tickcolor": "white"},
                "bar": {"color": "#667eea"},
                "steps": [
                    {"range": [0, target_cal * 0.5], "color": "rgba(255,100,100,0.2)"},
                    {"range": [target_cal * 0.5, target_cal], "color": "rgba(100,255,150,0.2)"},
                    {"range": [target_cal, target_cal * 1.3], "color": "rgba(255,165,0,0.2)"},
                ],
                "threshold": {"line": {"color": "#f093fb", "width": 3}, "value": target_cal}
            },
            number={"font": {"color": "white"}}
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"}, height=280, margin=dict(t=40, b=10)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Macros Donut
    with col2:
        macro_vals = [dn["protein"], dn["carbs"], dn["fat"]]
        macro_labels = ["Protein", "Carbohydrates", "Fat"]
        colors = ["#667eea", "#f093fb", "#fda085"]

        if sum(macro_vals) == 0:
            macro_vals = [target_protein, target_carbs, target_fat]
            title_text = "Target Macro Split"
        else:
            title_text = "Today's Macro Split"

        fig_donut = go.Figure(go.Pie(
            labels=macro_labels, values=macro_vals,
            hole=0.6, marker_colors=colors,
            textinfo="label+percent",
            textfont={"color": "white", "size": 12}
        ))
        fig_donut.update_layout(
            title={"text": title_text, "font": {"color": "white"}},
            paper_bgcolor="rgba(0,0,0,0)",
            legend={"font": {"color": "white"}},
            height=280, margin=dict(t=50, b=10)
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # Nutrient Progress Bars
    st.markdown("### 🎯 Daily Nutrient Goals")
    nutrients = [
        ("🔥 Calories", dn["calories"], target_cal, "kcal", "#667eea"),
        ("💪 Protein", dn["protein"], target_protein, "g", "#f093fb"),
        ("🌾 Carbohydrates", dn["carbs"], target_carbs, "g", "#fda085"),
        ("🥑 Fat", dn["fat"], target_fat, "g", "#4facfe"),
        ("🌿 Fiber", dn["fiber"], 30, "g", "#43e97b"),
    ]

    fig_bar = go.Figure()
    for name, val, target, unit, color in nutrients:
        pct = min(100, (val / target * 100)) if target > 0 else 0
        fig_bar.add_trace(go.Bar(
            name=name, x=[pct], y=[name],
            orientation="h",
            marker_color=color,
            text=f"{val}{unit} / {target}{unit}",
            textposition="outside",
            textfont={"color": "white"}
        ))

    fig_bar.update_layout(
        barmode="overlay",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis={"title": "% of Daily Goal", "range": [0, 120], "tickcolor": "white", "color": "white"},
        yaxis={"color": "white"},
        showlegend=False,
        height=300,
        margin=dict(l=20, r=80, t=10, b=40),
        font={"color": "white"}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Weekly Sample Data
    st.markdown("### 📅 Weekly Calorie Overview (Sample)")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    import random
    random.seed(42)
    sample_cal = [random.randint(1400, 2000) for _ in days]
    sample_cal[-1] = dn["calories"] if dn["calories"] > 0 else 1650

    fig_weekly = go.Figure()
    fig_weekly.add_trace(go.Bar(
        x=days, y=sample_cal, name="Calories",
        marker=dict(color=["#667eea"] * 6 + ["#f093fb"],
                    line=dict(color="rgba(255,255,255,0.2)", width=1))
    ))
    fig_weekly.add_hline(y=target_cal, line_dash="dash",
                          line_color="#fda085", annotation_text=f"Target: {target_cal} kcal",
                          annotation_font_color="white")
    fig_weekly.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis={"color": "white"}, yaxis={"color": "white"},
        showlegend=False, height=280,
        margin=dict(t=20, b=20),
        font={"color": "white"}
    )
    st.plotly_chart(fig_weekly, use_container_width=True)

    # IBM Branding Footer
    st.divider()
    st.markdown("""
    <div style='text-align:center; padding: 1rem; color: rgba(255,255,255,0.4);'>
        <p>🤖 Powered by <b style='color:#667eea;'>IBM Granite 3.3-8B Instruct</b> via HuggingFace Inference API</p>
        <p style='font-size:0.8rem;'>Multi-Agent RAG Pipeline | LangChain Orchestration | ChromaDB Vector Store</p>
        <p style='font-size:0.75rem;'>IBM Internship Project — AI-Powered Nutrition Agent</p>
    </div>
    """, unsafe_allow_html=True)
