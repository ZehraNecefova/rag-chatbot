# frontend/app.py
import streamlit as st
import httpx
import asyncio

st.set_page_config(page_title="RAG Chatbot", layout="wide")

# ---------------- Custom CSS ----------------
st.markdown(
    """
<style>
body, .stApp { background-color: #FFFFFF; }
section[data-testid="stSidebar"] { background-color: #EBDFEB !important; }
.user-bubble { background-color: #DCF8C6; padding: 10px 15px; border-radius: 15px; margin: 8px 0; text-align: right; font-size: 16px; }
.bot-bubble { background-color: #EBDFEB; padding: 10px 15px; border-radius: 15px; margin: 8px 0; text-align: left; font-size: 16px; }
input[type="text"] { background-color: #EBDFEB !important; color: #000000 !important; border: 1px solid #EBDFEB !important; border-radius: 8px !important; padding: 8px !important; }
input[aria-label="📜 System Instruction"] { background-color: #FFFFFF !important; color: #000000 !important; border: 1px solid #CCCCCC !important; border-radius: 8px !important; padding: 6px !important; }
.chat-title { font-size: 38px !important; font-weight: bold; color: #4B0082; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------- Sidebar ----------------
with st.sidebar:
    st.title("🤖 RAG Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chats" not in st.session_state:
        st.session_state.chats = []
    if "current_chat_index" not in st.session_state:
        st.session_state.current_chat_index = None

    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.session_state.current_chat_index = None

    if st.button("🗑️ Delete This Chat"):
        if st.session_state.current_chat_index is not None:
            del st.session_state.chats[st.session_state.current_chat_index]
            st.session_state.messages = []
            st.session_state.current_chat_index = None

    model = st.selectbox("⚙️ Choose model", ["Claude 3.7 Sonnet", "Claude 2"])
    system_instruction = st.text_input("📜 System Instruction", "")

    st.subheader("📂 Chat History")
    for i, chat in enumerate(st.session_state.chats):
        if st.button(f"💬 Chat {i+1}"):
            st.session_state.messages = chat.copy()
            st.session_state.current_chat_index = i

# ---------------- Main Chat Area ----------------
# ---------------- Main Chat Area ----------------
# ---------------- Main Chat Area ----------------
st.markdown("<div class='chat-title'>💬 Chat</div>", unsafe_allow_html=True)

# Container for chat
messages_container = st.container()

# Show all previous messages (except the one currently being typed/streamed)
for message in st.session_state.messages:
    if message.get("bot"):  # only show completed messages
        if "user" in message:
            messages_container.markdown(
                f"<div class='user-bubble'>🧑 <b>You:</b><br>{message['user']}</div>",
                unsafe_allow_html=True,
            )
        if "bot" in message:
            messages_container.markdown(
                f"<div class='bot-bubble'>🤖 <b>Bot:</b><br>{message['bot']}</div>",
                unsafe_allow_html=True,
            )

# ---------------- Input Form ----------------
st.divider()
with st.form(key="chat_form"):
    user_input = st.text_input(
        "Type your message:",
        key="user_input",
        value="",
        placeholder="Enter your query",  # 👈 added placeholder
        label_visibility="collapsed",
    )
    send_button = st.form_submit_button("➤ Send")


if send_button and user_input:
    # Add new (incomplete) message
    st.session_state.messages.append({"user": user_input, "bot": ""})
    if st.session_state.current_chat_index is None:
        st.session_state.chats.append(st.session_state.messages.copy())
        st.session_state.current_chat_index = len(st.session_state.chats) - 1

    # Show the just-submitted user message immediately
    messages_container.markdown(
        f"<div class='user-bubble'>🧑 <b>You:</b><br>{user_input}</div>",
        unsafe_allow_html=True,
    )

    # Placeholder for streaming bot reply
    bot_placeholder = messages_container.empty()

    # ---------------- Streaming Bot Response ----------------
    async def stream_response():
        answer = ""
        try:
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream(
                    "POST",
                    "http://backend:8000/chat-stream",
                    json={
                        "question": user_input,
                        "model": model,
                        "system_instruction": system_instruction,
                    },
                ) as response:
                    async for chunk in response.aiter_text():
                        answer += chunk
                        bot_placeholder.markdown(
                            f"<div class='bot-bubble'>🤖 <b>Bot:</b><br>{answer}</div>",
                            unsafe_allow_html=True,
                        )
        except Exception as e:
            bot_placeholder.markdown(
                f"<div class='bot-bubble'>⚠️ Error: {e}</div>", unsafe_allow_html=True
            )

        # Save final answer into session_state
        st.session_state.messages[-1]["bot"] = answer
        st.session_state.chats[
            st.session_state.current_chat_index
        ] = st.session_state.messages.copy()

    asyncio.run(stream_response())
