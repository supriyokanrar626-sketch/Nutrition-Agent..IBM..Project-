# 🥗 NutriAgent AI — IBM-Powered Nutrition Intelligence Platform

> **IBM Internship Project** | Multi-Agent AI System | LangFlow + IBM Granite + RAG

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red)](https://streamlit.io)
[![IBM Granite](https://img.shields.io/badge/IBM-Granite%203.3--8B-054ADA)](https://huggingface.co/ibm-granite)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📌 Problem Statement

Good nutrition is the foundation of health, but individuals often struggle with diet planning, portion control, and tracking nutritional intake. Without personalized, real-time guidance, many fail to maintain balanced diets.

## 🎯 Solution Overview

An **AI-powered Multi-Agent Nutrition System** that delivers personalized dietary insights using:
- **IBM Granite 3.3-8B Instruct** model for AI reasoning
- **RAG Pipeline** (ChromaDB + Sentence Transformers) for accurate nutritional data retrieval
- **4 Specialized AI Agents** for comprehensive nutrition management
- **Interactive Dashboard** with real-time visualizations

---

## 🏗️ Architecture

```
User Input
    │
    ▼
┌─────────────────────────────────────────┐
│           Streamlit Dashboard           │
│  (Chat UI + Visualization Dashboard)   │
└────────────┬────────────────────────────┘
             │
     ┌───────┴────────┐
     │  Agent Router   │
     └───┬───┬───┬────┘
         │   │   │   │
    ┌────┘   │   │   └────────────────┐
    ▼        ▼   ▼                   ▼
┌──────┐ ┌──────┐ ┌──────────┐ ┌──────────┐
│Nutr. │ │Diet  │ │ Health   │ │Food Log  │
│Agent │ │Agent │ │ Advisory │ │& Feedback│
└──┬───┘ └──┬───┘ └────┬─────┘ └────┬─────┘
   │        │          │             │
   └────────┴──────────┴─────────────┘
                       │
              ┌────────┴────────┐
              │   IBM Granite   │
              │  3.3-8B Instruct│
              │ (HuggingFace)   │
              └────────┬────────┘
                       │
              ┌────────┴────────┐
              │   RAG Pipeline  │
              │ ChromaDB + FAISS│
              │ USDA Nutrition  │
              │    Database     │
              └─────────────────┘
```

---

## 🤖 Multi-Agent System

| Agent | Role | Technology |
|-------|------|-----------|
| **Nutrition Knowledge Agent** | Retrieves nutritional values (calories, macros, vitamins) via RAG | IBM Granite + ChromaDB |
| **Diet Recommendation Agent** | Generates personalized meal plans based on user profile | IBM Granite + BMR/TDEE |
| **Health Advisory Agent** | Disease-specific nutrition (diabetes, heart health) | IBM Granite + RAG |
| **Food Log & Feedback Agent** | Tracks meals, estimates nutrition, gives feedback | IBM Granite + Rule Engine |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **LLM Model** | IBM Granite 3.3-8B Instruct |
| **Model Access** | HuggingFace Inference API |
| **RAG Vector Store** | ChromaDB |
| **Embeddings** | sentence-transformers/all-MiniLM-L6-v2 |
| **Frontend** | Streamlit + Plotly |
| **Agent Orchestration** | LangChain |
| **Knowledge Base** | USDA + WHO Nutrition Data |

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/nutrition-agent.git
cd nutrition-agent
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Token
Get your **free** HuggingFace token from: https://huggingface.co/settings/tokens

Open `config.py` and replace:
```python
HF_TOKEN = "YOUR_HUGGINGFACE_TOKEN_HERE"
```

### 4. Run the Application
```bash
streamlit run app.py
```

Open your browser at: **http://localhost:8501**

---

## ✨ Features

- 🔬 **Nutrition Lookup** — Calories, macros, vitamins for any food via RAG
- 🍽️ **Personalized Diet Plans** — Based on age, weight, conditions, preferences
- 🏥 **Health Advisory** — Diabetes, heart health, PCOS, thyroid management
- 📝 **Meal Logging** — Log meals via text with instant AI feedback
- 📊 **Visual Dashboard** — Real-time charts, gauges, weekly trends
- 🧮 **BMR/TDEE Calculator** — Personalized calorie targets
- 🇮🇳 **Indian Food Support** — Dal, roti, biryani, idli and more

---

## 📁 Project Structure

```
nutrition-agent/
├── app.py                    # Main Streamlit application
├── config.py                 # Configuration & API keys
├── requirements.txt          # Python dependencies
├── agents/
│   ├── llm_helper.py         # IBM Granite API wrapper
│   ├── nutrition_agent.py    # Agent 1: Nutrition Knowledge
│   ├── diet_agent.py         # Agent 2: Diet Recommendation
│   ├── health_agent.py       # Agent 3: Health Advisory
│   └── food_log_agent.py     # Agent 4: Food Log & Feedback
├── rag/
│   └── knowledge_base.py     # ChromaDB RAG pipeline
└── data/
    └── nutrition_data.txt    # Nutrition knowledge base
```

---

## 👨‍💻 Author

**IBM Internship Project — 2025**  
Built with ❤️ using IBM Granite AI + LangChain + Streamlit

---

## 📄 License

MIT License — Free to use and modify.
