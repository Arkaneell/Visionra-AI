import streamlit as st
import time
from agent import EntrepreneurshipAgent

# Page config
st.set_page_config(
    page_title="Visionra AI",
    page_icon="🚀",
    layout="wide"
)

# Title
st.title("Visionra AI: AI for innovative solutions")

# Help text
HELP_TEXT = """
### Commands
- **reset** — Clear conversation history
- **help** — Show this message

### What you can ask
- Run a Lean Canvas for my B2B SaaS idea
- Evaluate this startup idea
- Pricing strategy for pre-seed
- Product-market fit frameworks
"""

# ✅ Cache agent (prevents reloading)
@st.cache_resource
def get_agent():
    return EntrepreneurshipAgent()

if "agent" not in st.session_state:
    st.session_state.agent = get_agent()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
with st.sidebar:
    st.header("⚙️ Controls")

    if st.button("🔄 Reset Conversation"):
        st.session_state.agent.reset()
        st.session_state.chat_history = []
        st.success("Conversation reset!")

    if st.button("❓ Help"):
        st.markdown(HELP_TEXT)

# Chat display
st.subheader("💬 Chat")

for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)

# ✅ Streaming function (makes UI feel faster)
def stream_response(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.01)

# User input
user_input = st.chat_input("Type your idea or question...")

if user_input:
    # Add user message
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").markdown(user_input)

    # Handle commands
    if user_input.lower() == "reset":
        st.session_state.agent.reset()
        st.session_state.chat_history = []
        st.rerun()

    elif user_input.lower() == "help":
        st.chat_message("assistant").markdown(HELP_TEXT)
        st.session_state.chat_history.append(("assistant", HELP_TEXT))

    else:
        # ✅ Better status (non-blocking feel)
        with st.status("🧠 Thinking...", expanded=False):
            try:
                response = st.session_state.agent.chat(user_input)
            except Exception as e:
                response = f"❌ Error: {str(e)}"

        # ✅ Stream response instead of dumping at once
        st.chat_message("assistant").write_stream(stream_response(response))

        # Save response
        st.session_state.chat_history.append(("assistant", response))

        # ✅ Limit history (prevents slowdown over time)
        st.session_state.chat_history = st.session_state.chat_history[-10:]
