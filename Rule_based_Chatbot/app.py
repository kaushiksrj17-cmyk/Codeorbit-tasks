"""
Task 1: Rule-Based Chatbot - Streamlit Web Application
======================================================
Web interface for the Python Rule-Based Chatbot using Streamlit.
Provides a modern chat UI, sidebar quick-actions, real-time session
state tracking, and seamless integration with chatbot.py.
"""

import streamlit as st
import datetime
from chatbot import process_message, get_help_menu

# Page configuration
st.set_page_config(
    page_title="Rule-Based Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    /* Main container styling */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(240, 244, 255, 0.8) 0%, rgba(255, 255, 255, 1) 90%);
    }
    
    /* Header badge styling */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 600;
        background: linear-gradient(135deg, #6366f1, #4f46e5);
        color: white;
        margin-bottom: 8px;
    }
    
    /* Card in sidebar */
    .sidebar-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "session" not in st.session_state:
    st.session_state.session = {
        "user_name": None,
        "history": []
    }

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I am your Python Rule-Based Chatbot. Type a greeting, ask for the date/time, tell me your name, or type **'help'** to see everything I can do!"
        }
    ]

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/bot.png", width=80)
    st.title("🤖 Chatbot Panel")
    st.caption("Internship Task 1: Rule-Based Chatbot")

    st.markdown("---")

    # Real-time Session Memory Display
    st.subheader("🧠 Session Memory")
    if st.session_state.session.get("user_name"):
        st.success(f"**Remembered Name:** {st.session_state.session['user_name']}")
    else:
        st.info("No name stored yet.\n*(Try: 'My name is [Your Name]')*")

    st.markdown("---")

    # Quick Suggestions
    st.subheader("💡 Quick Actions")
    st.write("Click any quick query to test:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("👋 Hello", use_container_width=True):
            st.session_state.pending_prompt = "Hello"
        if st.button("🕒 Time", use_container_width=True):
            st.session_state.pending_prompt = "What time is it?"
        if st.button("🎭 Joke", use_container_width=True):
            st.session_state.pending_prompt = "Tell me a joke"
        if st.button("❓ Who are you?", use_container_width=True):
            st.session_state.pending_prompt = "Who are you?"
    with col2:
        if st.button("📅 Date", use_container_width=True):
            st.session_state.pending_prompt = "What is today's date?"
        if st.button("🙋 My Name?", use_container_width=True):
            st.session_state.pending_prompt = "What is my name?"
        if st.button("🙏 Thanks", use_container_width=True):
            st.session_state.pending_prompt = "Thank you!"
        if st.button("📜 History", use_container_width=True):
            st.session_state.pending_prompt = "history"

    st.markdown("---")

    # Clear Conversation Button
    if st.button("🗑️ Clear Chat History", type="secondary", use_container_width=True):
        st.session_state.session["history"].clear()
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Conversation history cleared! How can I assist you now?"
            }
        ]
        st.rerun()

    with st.expander("ℹ️ Supported Rules / Help"):
        st.text(get_help_menu())


# ============================================================================
# MAIN CHAT INTERFACE
# ============================================================================

st.markdown('<span class="badge">Rule-Based Architecture</span>', unsafe_allow_html=True)
st.title("Python Rule-Based Chatbot")
st.write("An interactive conversational assistant driven purely by Python pattern matching and predefined logic.")

# Display existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Determine current user prompt (from text input or quick action button)
user_prompt = st.chat_input("Type your message here (e.g., 'Hello', 'My name is Alex', 'Joke')...")

if st.session_state.pending_prompt:
    user_prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

# Handle user submission
if user_prompt:
    # Append and render user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Process message using core chatbot engine
    response, should_exit = process_message(user_prompt, st.session_state.session)

    # If the user asked to clear history via text
    norm_prompt = user_prompt.strip().lower()
    if norm_prompt in ["clear history", "reset history", "clear chat"]:
        st.session_state.messages = [
            {"role": "assistant", "content": "Your conversation history has been cleared for this session."}
        ]
        st.rerun()

    # Append and render assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

    # If an exit command was entered
    if should_exit:
        st.warning("👋 The session has ended. To restart the conversation, refresh the browser page or use the Clear Chat History button.")
        st.stop()
