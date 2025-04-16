import streamlit as st
import requests
from voice import record_voice

# ---- CONFIG ----
st.set_page_config(page_title="AI Sales Chatbot", page_icon="🍭")
backend_base = "https://7cb0-34-87-140-21.ngrok-free.app"  # Replace with your actual URL
backend_url = backend_base + "/ask"
clear_url = backend_base + "/clear"

# ---- SESSION STATE ----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "transcribed_input" not in st.session_state:
    st.session_state.transcribed_input = ""
if "last_voice_input" not in st.session_state:
    st.session_state.last_voice_input = ""

# ---- CHAT DISPLAY ----
st.subheader("🗣️ Conversation")
chat_container = st.container()
with chat_container:
    for speaker, message in st.session_state.chat_history:
        st.markdown(f"**{speaker}:** {message}")
    st.divider()

# ---- INPUT SECTION ----
st.subheader("🎤 Ask Your Question")

with st.container():
    col1, col2 = st.columns([3, 2])

    with col1:
        with st.form("text_input_form", clear_on_submit=True):
            user_question = st.text_input(
                "Type your question here",
                key="user_input",
                value=st.session_state.transcribed_input
            )
            submitted = st.form_submit_button("📬 Ask")

            if submitted and user_question.strip():
                with st.spinner("Thinking..."):
                    try:
                        res = requests.post(backend_url, json={"username": "guest", "question": user_question})
                        answer = res.json().get("answer", "No answer received.")
                        st.session_state.chat_history.append(("🧑 You", user_question))
                        st.session_state.chat_history.append(("🤖 AI", answer))
                        st.session_state.transcribed_input = ""
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            elif submitted:
                st.warning("⚠️ Please enter a question.")

    with col2:
        st.write("")  # spacing
        transcribed_text = record_voice(language="en")

        if st.button("🗑️ Clear Conversation", key="clear_button"):
            st.session_state.chat_history = []
            st.session_state.transcribed_input = ""
            st.session_state.last_voice_input = ""
            try:
                requests.post(clear_url, json={"username": "guest"})
            except:
                st.warning("⚠️ Failed to clear memory on server.")
            st.success("✅ Conversation cleared!")
            st.rerun()

        if transcribed_text and transcribed_text != st.session_state.last_voice_input:
            st.session_state.last_voice_input = transcribed_text
            st.session_state.chat_history.append(("🧑 You", transcribed_text))
            with st.spinner("🧠 Thinking..."):
                try:
                    res = requests.post(backend_url, json={"username": "guest", "question": transcribed_text})
                    answer = res.json().get("answer", "No answer received.")
                    st.session_state.chat_history.append(("🤖 AI", answer))
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

