import streamlit as st
from agent import EntrepreneurshipAgent

# Page config
st.set_page_config(
    page_title="Entrepreneurship Intelligence Agent",
    page_icon="🚀",
    layout="wide"
)

# Title
st.title("🚀 Entrepreneurship & Innovation Intelligence Agent")

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

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = EntrepreneurshipAgent()

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
    if role == "user":
        st.chat_message("user").markdown(message)
    else:
        st.chat_message("assistant").markdown(message)

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
        st.experimental_rerun()

    elif user_input.lower() == "help":
        st.chat_message("assistant").markdown(HELP_TEXT)
        st.session_state.chat_history.append(("assistant", HELP_TEXT))

    else:
        # Generate response
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.agent.chat(user_input)
            except Exception as e:
                response = f"❌ Error: {str(e)}"

        # Show response
        st.chat_message("assistant").markdown(response)
        st.session_state.chat_history.append(("assistant", response))
