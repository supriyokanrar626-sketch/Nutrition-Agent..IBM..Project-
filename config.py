
# ============================================================
# IBM Nutrition Agent - Configuration
# ============================================================
# Replace HF_TOKEN with your HuggingFace token from:
# https://huggingface.co/settings/tokens
# ============================================================

import os

# --- HuggingFace Token (Free) ---
HF_TOKEN = os.environ.get("HF_TOKEN", "your HuggingFace token")

# --- IBM Granite Model (via HuggingFace) ---
GRANITE_MODEL_ID = "ibm-granite/granite-4.0-8b-instruct"

# --- HuggingFace Inference API Endpoint ---
HF_API_URL = f"https://api-inference.huggingface.co/models/{GRANITE_MODEL_ID}"

# --- Embedding Model ---
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# --- ChromaDB Settings ---
CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "nutrition_knowledge"

# --- App Settings ---
APP_TITLE = "NutriAgent AI"
APP_SUBTITLE = "IBM-Powered Nutrition Intelligence Platform"
APP_VERSION = "1.0.0"

# --- Nutrition API (Free USDA FoodData Central) ---
USDA_API_KEY = "DEMO_KEY"  # Free demo key — works for testing
USDA_BASE_URL = "https://api.nal.usda.gov/fdc/v1"
