# import streamlit as st
# import google.generativeai as genai
# from google.api_core import exceptions as google_exceptions
# import os
# from dotenv import load_dotenv
# import sqlite3
# from datetime import datetime
# import random

# # =========================
# # LOAD ENVIRONMENT VARIABLES
# # =========================
# load_dotenv()

# # =========================
# # PAGE CONFIGURATION
# # =========================
# st.set_page_config(
#     page_title="CharmBot - Flirting Assistant",
#     page_icon="💕",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # =========================
# # DATABASE INITIALIZATION
# # =========================
# DB_PATH = "charmbot_history.db"

# def init_db():
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS conversations (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             timestamp TEXT,
#             message TEXT,
#             style TEXT,
#             context TEXT,
#             gender_pref TEXT,
#             response TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()

# def save_to_db(message, style, context, gender_pref, response):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO conversations (timestamp, message, style, context, gender_pref, response)
#         VALUES (?, ?, ?, ?, ?, ?)
#     ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message, style, context, gender_pref, response))
#     conn.commit()
#     conn.close()

# def load_history():
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute('SELECT timestamp, message, response, style, context, gender_pref FROM conversations ORDER BY id DESC')
#     data = cursor.fetchall()
#     conn.close()
#     return data

# init_db()

# # =========================
# # CUSTOM THEME
# # =========================
# st.markdown("""
# <style>
#     /* Main app background */
#     .stApp {
#         background: linear-gradient(135deg, #0a0e0a 0%, #1a1f1a 100%) !important;
#     }
    
#     /* Remove white header bar */
#     header[data-testid="stHeader"] {
#         background: transparent !important;
#         background-color: transparent !important;
#     }
    
#     /* Main content container */
#     .block-container {
#         background: transparent !important;
#         padding-top: 2rem !important;
#         color: #00ff87 !important;
#     }
    
#     /* All text colors */
#     h1, h2, h3, h4, h5, h6, p, label, span, div {
#         color: #00ff87 !important;
#     }
    
#     /* Title styling */
#     h1 {
#         text-shadow: 0 0 20px rgba(0, 255, 135, 0.3) !important;
#     }
    
#     /* Text inputs and textareas */
#     textarea, input, select {
#         background: #1a1f1a !important;
#         color: #00ff87 !important;
#         border: 2px solid #00ff87 !important;
#         border-radius: 10px !important;
#     }
    
#     /* Selectbox styling */
#     [data-baseweb="select"] > div {
#         background: #1a1f1a !important;
#         border: 2px solid #00ff87 !important;
#         border-radius: 10px !important;
#     }
    
#     /* Dropdown options */
#     [role="listbox"] {
#         background-color: #1a1f1a !important;
#     }
    
#     [role="option"] {
#         color: #00ff87 !important;
#         background-color: #1a1f1a !important;
#     }
    
#     [role="option"]:hover {
#         background-color: #2a4d2a !important;
#     }
    
#     /* Buttons */
#     .stButton>button {
#         background: linear-gradient(135deg, #1a4d2e 0%, #0d2818 100%);
#         color: #00ff87 !important;
#         border: 2px solid #00ff87 !important;
#         border-radius: 8px !important;
#         font-weight: bold !important;
#         transition: all 0.3s !important;
#     }
    
#     .stButton>button:hover {
#         background: linear-gradient(135deg, #00ff87 0%, #00cc6f 100%) !important;
#         color: #0a0e0a !important;
#         transform: scale(1.05) !important;
#     }
    
#     /* Response box */
#     .response-box {
#         background: linear-gradient(135deg, #1a4d2e 0%, #0d2818 100%);
#         padding: 1.5rem;
#         border-radius: 10px;
#         border: 2px solid #00ff87;
#         color: #e0ffe0;
#         font-size: 1.15rem;
#         margin-top: 1rem;
#         box-shadow: 0 0 15px rgba(0, 255, 135, 0.3);
#     }
    
#     /* History card */
#     .history-card {
#         border: 2px solid #00ff87;
#         border-radius: 10px;
#         padding: 1rem;
#         margin-bottom: 1rem;
#         background: linear-gradient(135deg, #0d2818 0%, #0a0e0a 100%);
#         box-shadow: 0 0 10px rgba(0,255,135,0.2);
#     }
    
#     /* Sidebar styling */
#     [data-testid="stSidebar"] {
#         background: linear-gradient(180deg, #0f1810 0%, #0a0e0a 100%) !important;
#         border-right: 2px solid #00ff87 !important;
#     }
    
#     [data-testid="stSidebar"] * {
#         color: #e0ffe0 !important;
#     }
    
#     /* Sidebar toggle button */
#     [data-testid="collapsedControl"] {
#         background-color: #1a4d2e !important;
#         border: 2px solid #00ff87 !important;
#         border-radius: 8px !important;
#     }
    
#     [data-testid="collapsedControl"]:hover {
#         background-color: #2a6d4e !important;
#     }
    
#     [data-testid="collapsedControl"] svg {
#         fill: #00ff87 !important;
#     }
    
#     /* Radio buttons */
#     [data-testid="stSidebar"] [data-baseweb="radio"] label {
#         color: #00ff87 !important;
#     }
    
#     /* Success/Info/Warning boxes */
#     .stSuccess, .stInfo, .stWarning {
#         background-color: #1a4d2e !important;
#         color: #00ff87 !important;
#     }
    
#     /* Expander */
#     .streamlit-expanderHeader {
#         background-color: #1a4d2e !important;
#         color: #00ff87 !important;
#         border: 1px solid #00ff87 !important;
#     }
    
#     .streamlit-expanderContent {
#         background-color: #0d2818 !important;
#         color: #e0ffe0 !important;
#     }
    
#     /* Caption text */
#     .stCaption {
#         color: #00ff87 !important;
#         opacity: 0.8 !important;
#     }
    
#     /* Remove any remaining white backgrounds */
#     div[data-testid="stVerticalBlock"] > div {
#         background-color: transparent !important;
#     }
# </style>
# """, unsafe_allow_html=True)

# # =========================
# # CONFIGURATIONS
# # =========================
# CONVERSATION_STYLES = {
#     "playful": "Be playful, teasing, and fun. Light humor and wit. Keep it flirty but lighthearted.",
#     "romantic": "Be romantic, sweet, and charming. Focus on genuine compliments and emotional connection.",
#     "witty": "Be clever, sharp, and intellectually flirty. Use wordplay, puns, and smart humor.",
#     "confident": "Be bold, direct, and self-assured. Show confidence without arrogance.",
#     "mysterious": "Be intriguing and enigmatic. Leave them curious and wanting to know more.",
#     "smooth": "Be suave and effortlessly cool. Use smooth lines that flow naturally."
# }

# CONTEXTS = {
#     "first_message": "This is likely a first interaction. Be charming but not too forward.",
#     "ongoing": "Part of an ongoing conversation. Build on established rapport.",
#     "dating_app": "From a dating app. Be engaging and show genuine interest.",
#     "casual": "Casual interaction that could become flirty.",
#     "text_reply": "A text message reply. Keep it conversational."
# }

# FALLBACK_RESPONSES = {
#     "playful": ["Well, that's definitely one way to get my attention! 😏", "I like where this conversation is heading...", "You're trouble, aren't you? 😉"],
#     "romantic": ["That's really sweet of you ✨", "You have a way with words that's charming", "I'm genuinely smiling at my phone right now"],
#     "witty": ["Interesting point... I suspect there's more to you than meets the eye", "I see what you did there, clever!", "That's either very clever or naturally charming"],
#     "confident": ["I like someone who knows what they want", "Direct and to the point - I respect that", "Confidence is attractive, and you have it"],
#     "mysterious": ["Now you have me curious... tell me more", "There's more to this story, isn't there?", "You're keeping me guessing, I like it"],
#     "smooth": ["That was smoother than expected... impressive", "I see you have some moves - intrigued", "Well played... you know how to make an impression"]
# }

# # =========================
# # GEMINI INITIALIZATION
# # =========================
# def initialize_gemini():
#     api_key = os.getenv("GOOGLE_API_KEY")
#     if not api_key:
#         st.error("❌ GOOGLE_API_KEY not found in .env file.")
#         return None
    
#     try:
#         genai.configure(api_key=api_key)
#         model = genai.GenerativeModel("gemini-2.0-flash-exp")
#         model.generate_content("Hello!")  # test connection
#         st.sidebar.success("✅ Gemini Connected: gemini-2.0-flash-exp")
#         return model
#     except Exception as e:
#         st.sidebar.error(f"⚠️ Gemini API Error: {str(e)}")
#         return None

# # =========================
# # PROMPT GENERATION
# # =========================
# def build_prompt(message, style, context, gender_pref):
#     return f"""
# You are an expert at crafting charming, flirty responses.

# STYLE: {CONVERSATION_STYLES[style]}
# CONTEXT: {CONTEXTS[context]}
# TARGET: {gender_pref}

# MESSAGE: "{message}"

# RULES:
# - 1-2 sentences maximum
# - Confident but respectful
# - Make them smile and want to respond
# - Subtle flirtation appropriate to context
# - Natural, genuine tone
# - No pickup lines
# """

# def generate_response(model, message, style, context, gender_pref):
#     if not model:
#         return random.choice(FALLBACK_RESPONSES[style])
#     try:
#         prompt = build_prompt(message, style, context, gender_pref)
#         response = model.generate_content(prompt)
#         return response.text.strip()
#     except Exception:
#         return random.choice(FALLBACK_RESPONSES[style])

# # =========================
# # MAIN APP
# # =========================
# def main():
#     # Initialize session state
#     if 'current_message' not in st.session_state:
#         st.session_state['current_message'] = ""
#     if 'current_response' not in st.session_state:
#         st.session_state['current_response'] = ""
    
#     st.title("💖 CharmBot - Your AI Wingman")
#     st.caption("Craft the perfect flirty response ✨")

#     model = initialize_gemini()

#     # Sidebar Navigation
#     st.sidebar.header("🧭 Navigation")
#     page = st.sidebar.radio("Go to:", ["💬 Chat", "🕓 View History"])

#     # Sidebar Configuration Toggle
#     st.sidebar.markdown("---")
#     with st.sidebar.expander("⚙️ Configuration", expanded=True):
#         style = st.selectbox("🎭 Style", list(CONVERSATION_STYLES.keys()), index=0)
#         context = st.selectbox("💬 Context", list(CONTEXTS.keys()), index=0)
#         gender_pref = st.selectbox("👥 Talking to", ["anyone", "women", "men", "non-binary individuals"], index=0)

#     # ================= CHAT PAGE =================
#     if page == "💬 Chat":
#         col1, col2 = st.columns([2.5, 1.5])
        
#         with col1:
#             message = st.text_area(
#                 "💌 Enter the message you received:",
#                 value=st.session_state['current_message'],
#                 placeholder="Hey! How's your day going?",
#                 height=120,
#                 key="message_input"
#             )

#             if st.button("✨ Generate Reply", use_container_width=True):
#                 if not message.strip():
#                     st.warning("⚠️ Please enter a message first.")
#                 else:
#                     with st.spinner("Crafting your perfect reply... 💫"):
#                         response = generate_response(model, message, style, context, gender_pref)
#                         st.session_state['current_response'] = response
#                         save_to_db(message, style, context, gender_pref, response)

#             # Display response
#             if st.session_state['current_response']:
#                 st.markdown("### 🎯 Your Charming Reply:")
#                 st.markdown(f'<div class="response-box">{st.session_state["current_response"]}</div>', unsafe_allow_html=True)
                
#                 col_copy1, col_copy2, col_copy3 = st.columns([1, 2, 1])
#                 with col_copy2:
#                     if st.button("📋 Copy to Clipboard", use_container_width=True):
#                         st.code(st.session_state['current_response'], language=None)
#                         st.success("✅ Use Ctrl+C to copy from the box above")

#         with col2:
#             st.header("💡 Quick Examples")
#             st.caption("*Click to auto-load*")
            
#             examples = [
#                 "Hey! How's your day going?",
#                 "What are you up to this weekend?",
#                 "I saw your profile and had to say hi",
#                 "That's actually really funny 😂",
#                 "Coffee date tomorrow?",
#                 "You seem interesting...",
#                 "Good morning! ☀️",
#                 "How was your weekend?",
#                 "I love your style!",
#                 "What's your favorite way to spend a Friday night?"
#             ]
            
#             for i, example in enumerate(examples):
#                 if st.button(f"📝 {example}", key=f"ex_{i}", use_container_width=True):
#                     st.session_state['current_message'] = example
#                     with st.spinner("✨"):
#                         response = generate_response(model, example, style, context, gender_pref)
#                         st.session_state['current_response'] = response
#                         save_to_db(example, style, context, gender_pref, response)
#                     st.rerun()

#     # ================= HISTORY PAGE =================
#     elif page == "🕓 View History":
#         st.subheader("🧾 Your Conversation History")
#         history = load_history()
#         if not history:
#             st.info("No conversation history yet. Start chatting!")
#         else:
#             for row in history:
#                 timestamp, msg, resp, style_h, ctx, gender = row
#                 st.markdown(f"""
#                 <div class="history-card">
#                     <p><b>🕒 {timestamp}</b></p>
#                     <p><b>💌 Message:</b> {msg}</p>
#                     <p><b>✨ Reply:</b> {resp}</p>
#                     <p><b>🎭 Style:</b> {style_h.title()} | <b>💬 Context:</b> {ctx} | <b>👥 Target:</b> {gender}</p>
#                 </div>
#                 """, unsafe_allow_html=True)

#     st.markdown("---")
#     st.markdown('<div style="text-align:center; color:#00ff87; opacity:0.8;">🌟 Powered by Google Gemini AI 💕</div>', unsafe_allow_html=True)


# if __name__ == "__main__":
#     main()






import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
import os
from dotenv import load_dotenv
import sqlite3
from datetime import datetime
import random

# =========================
# LOAD ENVIRONMENT VARIABLES
# =========================
load_dotenv()

# =========================
# PAGE CONFIGURATION
# =========================
st.set_page_config(
    page_title="CharmBot - Flirting Assistant",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# DATABASE INITIALIZATION
# =========================
DB_PATH = "charmbot_history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            message TEXT,
            style TEXT,
            context TEXT,
            gender_pref TEXT,
            response TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(message, style, context, gender_pref, response):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO conversations (timestamp, message, style, context, gender_pref, response)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message, style, context, gender_pref, response))
    conn.commit()
    conn.close()

def load_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, message, response, style, context, gender_pref FROM conversations ORDER BY id DESC')
    data = cursor.fetchall()
    conn.close()
    return data

init_db()

# =========================
# CUSTOM THEME
# =========================
st.markdown("""
<style>
/* ============================= */
/* 🌙 GLOBAL DARK NEON THEME */
/* ============================= */

/* Main app background */
.stApp {
    background: linear-gradient(135deg, #0a0e0a 0%, #1a1f1a 100%) !important;
}

/* Remove white header bar */
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* Main content container */
.block-container {
    background: transparent !important;
    padding-top: 2rem !important;
    color: #00ff87 !important;
}

/* Typography */
h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: #00ff87 !important;
}

h1 {
    text-shadow: 0 0 20px rgba(0, 255, 135, 0.3) !important;
}

/* Inputs and textareas */
textarea, input, select {
    background: #1a1f1a !important;
    color: #00ff87 !important;
    border: 2px solid #00ff87 !important;
    border-radius: 10px !important;
}

/* Selectbox styling */
[data-baseweb="select"] > div {
    background: #1a1f1a !important;
    border: 2px solid #00ff87 !important;
    border-radius: 10px !important;
}

/* Dropdown options */
[role="listbox"] {
    background-color: #1a1f1a !important;
}
[role="option"] {
    color: #00ff87 !important;
    background-color: #1a1f1a !important;
}
[role="option"]:hover {
    background-color: #2a4d2a !important;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #1a4d2e 0%, #0d2818 100%) !important;
    color: #00ff87 !important;
    border: 2px solid #00ff87 !important;
    border-radius: 8px !important;
    font-weight: bold !important;
    transition: all 0.3s ease !important;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #00ff87 0%, #00cc6f 100%) !important;
    color: #0a0e0a !important;
    transform: scale(1.05) !important;
}

/* Response box */
.response-box {
    background: linear-gradient(135deg, #1a4d2e 0%, #0d2818 100%);
    padding: 1.5rem;
    border-radius: 10px;
    border: 2px solid #00ff87;
    color: #e0ffe0;
    font-size: 1.15rem;
    margin-top: 1rem;
    box-shadow: 0 0 15px rgba(0, 255, 135, 0.3);
}

/* History card */
.history-card {
    border: 2px solid #00ff87;
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #0d2818 0%, #0a0e0a 100%);
    box-shadow: 0 0 10px rgba(0,255,135,0.2);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1810 0%, #0a0e0a 100%) !important;
    border-right: 2px solid #00ff87 !important;
}
[data-testid="stSidebar"] * {
    color: #e0ffe0 !important;
}

/* Sidebar toggle */
[data-testid="collapsedControl"] {
    background-color: #1a4d2e !important;
    border: 2px solid #00ff87 !important;
    border-radius: 8px !important;
}
[data-testid="collapsedControl"]:hover {
    background-color: #2a6d4e !important;
}
[data-testid="collapsedControl"] svg {
    fill: #00ff87 !important;
}

/* Sidebar radio */
[data-testid="stSidebar"] [data-baseweb="radio"] label {
    color: #00ff87 !important;
}

/* Status boxes */
.stSuccess, .stInfo, .stWarning {
    background-color: #1a4d2e !important;
    color: #00ff87 !important;
}

/* ============================= */
/* ⚙️ FIXED EXPANDER (NO WHITE FLASH) */
/* ============================= */

/* ============================= */
/* ⚙️ FIXED EXPANDER (NO WHITE FLASH) */
/* ============================= */

/* Base expander button - ALWAYS black */
section[data-testid="stExpander"] div[role="button"] {
    background-color: #000000 !important;
    color: #00ff87 !important;
    border: 1px solid #00ff87 !important;
    border-radius: 8px !important;
    box-shadow: none !important;
    transition: none !important;
}

/* Force black on ALL states - no exceptions */
section[data-testid="stExpander"] div[role="button"]:hover,
section[data-testid="stExpander"] div[role="button"]:focus,
section[data-testid="stExpander"] div[role="button"]:active,
section[data-testid="stExpander"] div[role="button"][aria-expanded="true"],
section[data-testid="stExpander"] div[role="button"][aria-expanded="false"] {
    background-color: #000000 !important;
    color: #00ff87 !important;
    box-shadow: none !important;
    transition: none !important;
}

/* Target any child divs that might be causing the white flash */
section[data-testid="stExpander"] div[role="button"] > div,
section[data-testid="stExpander"] div[role="button"] > div > *,
section[data-testid="stExpander"] div[role="button"] * {
    background-color: transparent !important;
    color: #00ff87 !important;
}

/* Expander wrapper */
section[data-testid="stExpander"] {
    background-color: transparent !important;
}

/* Expander content area */
section[data-testid="stExpander"] div[data-testid="stExpanderContent"] {
    background-color: #0d2818 !important;
    color: #e0ffe0 !important;
    border: 1px solid #00ff87 !important;
    border-top: none !important;
    box-shadow: inset 0 0 10px rgba(0,255,135,0.15);
}

/* Captions */
.stCaption {
    color: #00ff87 !important;
    opacity: 0.8 !important;
}

/* Remove stray white divs */
div[data-testid="stVerticalBlock"] > div {
    background-color: transparent !important;
}
</style>
""", unsafe_allow_html=True)


# =========================
# CONFIGURATIONS
# =========================
CONVERSATION_STYLES = {
    "playful": "Be playful, teasing, and fun. Light humor and wit. Keep it flirty but lighthearted.",
    "romantic": "Be romantic, sweet, and charming. Focus on genuine compliments and emotional connection.",
    "witty": "Be clever, sharp, and intellectually flirty. Use wordplay, puns, and smart humor.",
    "confident": "Be bold, direct, and self-assured. Show confidence without arrogance.",
    "mysterious": "Be intriguing and enigmatic. Leave them curious and wanting to know more.",
    "smooth": "Be suave and effortlessly cool. Use smooth lines that flow naturally."
}

CONTEXTS = {
    "first_message": "This is likely a first interaction. Be charming but not too forward.",
    "ongoing": "Part of an ongoing conversation. Build on established rapport.",
    "dating_app": "From a dating app. Be engaging and show genuine interest.",
    "casual": "Casual interaction that could become flirty.",
    "text_reply": "A text message reply. Keep it conversational."
}

FALLBACK_RESPONSES = {
    "playful": ["Well, that's definitely one way to get my attention! 😏", "I like where this conversation is heading...", "You're trouble, aren't you? 😉"],
    "romantic": ["That's really sweet of you ✨", "You have a way with words that's charming", "I'm genuinely smiling at my phone right now"],
    "witty": ["Interesting point... I suspect there's more to you than meets the eye", "I see what you did there, clever!", "That's either very clever or naturally charming"],
    "confident": ["I like someone who knows what they want", "Direct and to the point - I respect that", "Confidence is attractive, and you have it"],
    "mysterious": ["Now you have me curious... tell me more", "There's more to this story, isn't there?", "You're keeping me guessing, I like it"],
    "smooth": ["That was smoother than expected... impressive", "I see you have some moves - intrigued", "Well played... you know how to make an impression"]
}

# =========================
# GEMINI INITIALIZATION
# =========================
def initialize_gemini():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("❌ GOOGLE_API_KEY not found in .env file.")
        return None
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        model.generate_content("Hello!")  # test connection
        st.sidebar.success("✅ Gemini Connected: gemini-2.0-flash-exp")
        return model
    except Exception as e:
        st.sidebar.error(f"⚠️ Gemini API Error: {str(e)}")
        return None

# =========================
# PROMPT GENERATION
# =========================
def build_prompt(message, style, context, gender_pref):
    return f"""
You are an expert at crafting charming, flirty responses.

STYLE: {CONVERSATION_STYLES[style]}
CONTEXT: {CONTEXTS[context]}
TARGET: {gender_pref}

MESSAGE: "{message}"

RULES:
- 1-2 sentences maximum
- Confident but respectful
- Make them smile and want to respond
- Subtle flirtation appropriate to context
- Natural, genuine tone
- No pickup lines
"""

def generate_response(model, message, style, context, gender_pref):
    if not model:
        return random.choice(FALLBACK_RESPONSES[style])
    try:
        prompt = build_prompt(message, style, context, gender_pref)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return random.choice(FALLBACK_RESPONSES[style])

# =========================
# MAIN APP
# =========================
def main():
    # Initialize session state
    if 'current_message' not in st.session_state:
        st.session_state['current_message'] = ""
    if 'current_response' not in st.session_state:
        st.session_state['current_response'] = ""
    
    st.title("💖 CharmBot - Your AI Wingman")
    st.caption("Craft the perfect flirty response ✨")

    model = initialize_gemini()

    # Sidebar Navigation
    st.sidebar.header("🧭 Navigation")
    page = st.sidebar.radio("Go to:", ["💬 Chat", "🕓 View History"])

    # Sidebar Configuration Toggle
    st.sidebar.markdown("---")
    with st.sidebar.expander("⚙️ Configuration", expanded=True):
        style = st.selectbox("🎭 Style", list(CONVERSATION_STYLES.keys()), index=0)
        context = st.selectbox("💬 Context", list(CONTEXTS.keys()), index=0)
        gender_pref = st.selectbox("👥 Talking to", ["anyone", "women", "men", "non-binary individuals"], index=0)

    # ================= CHAT PAGE =================
    if page == "💬 Chat":
        col1, col2 = st.columns([2.5, 1.5])
        
        with col1:
            message = st.text_area(
                "💌 Enter the message you received:",
                value=st.session_state['current_message'],
                placeholder="Hey! How's your day going?",
                height=120,
                key="message_input"
            )

            if st.button("✨ Generate Reply", use_container_width=True):
                if not message.strip():
                    st.warning("⚠️ Please enter a message first.")
                else:
                    with st.spinner("Crafting your perfect reply... 💫"):
                        response = generate_response(model, message, style, context, gender_pref)
                        st.session_state['current_response'] = response
                        save_to_db(message, style, context, gender_pref, response)

            # Display response
            if st.session_state['current_response']:
                st.markdown("### 🎯 Your Charming Reply:")
                st.markdown(f'<div class="response-box">{st.session_state["current_response"]}</div>', unsafe_allow_html=True)
                
                # Copy functionality using st.code
                st.code(st.session_state['current_response'], language=None)

        with col2:
            st.header("💡 Quick Examples")
            st.caption("*Click to auto-load*")
            
            examples = [
                "Hey! How's your day going?",
                "What are you up to this weekend?",
                "I saw your profile and had to say hi",
                "That's actually really funny 😂",
                "Coffee date tomorrow?",
                "You seem interesting...",
                "Good morning! ☀️",
                "How was your weekend?",
                "I love your style!",
                "What's your favorite way to spend a Friday night?"
            ]
            
            for i, example in enumerate(examples):
                if st.button(f"📝 {example}", key=f"ex_{i}", use_container_width=True):
                    st.session_state['current_message'] = example
                    with st.spinner("✨"):
                        response = generate_response(model, example, style, context, gender_pref)
                        st.session_state['current_response'] = response
                        save_to_db(example, style, context, gender_pref, response)
                    st.rerun()

    # ================= HISTORY PAGE =================
    elif page == "🕓 View History":
        st.subheader("🧾 Your Conversation History")
        history = load_history()
        if not history:
            st.info("No conversation history yet. Start chatting!")
        else:
            for row in history:
                timestamp, msg, resp, style_h, ctx, gender = row
                st.markdown(f"""
                <div class="history-card">
                    <p><b>🕒 {timestamp}</b></p>
                    <p><b>💌 Message:</b> {msg}</p>
                    <p><b>✨ Reply:</b> {resp}</p>
                    <p><b>🎭 Style:</b> {style_h.title()} | <b>💬 Context:</b> {ctx} | <b>👥 Target:</b> {gender}</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="text-align:center; color:#00ff87; opacity:0.8;">🌟 Powered by Google Gemini AI 💕</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()