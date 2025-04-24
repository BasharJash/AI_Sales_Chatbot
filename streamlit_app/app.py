import streamlit as st
import requests
import base64
import os
import streamlit.components.v1 as components
from voice import record_voice  # Make sure voice.py is in the same directory

# ---- CONFIG ----
st.set_page_config(page_title="Gymshark AI Assistant", layout="wide")
backend_base = "https://d6ce-213-173-110-155.ngrok-free.app"  # Replace with your actual backend URL
backend_url = backend_base + "/ask"
clear_url = backend_base + "/clear"

# ---- LOGO SECTION ----
logo_path = os.path.join(os.path.dirname(__file__), "gymshark_logo.png")
if os.path.exists(logo_path):
    logo_data = base64.b64encode(open(logo_path, "rb").read()).decode()
    st.markdown(
        f"""
        <div style='text-align: center;'>
            <img src="data:image/png;base64,{logo_data}" width="500" />
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("""
<h1 style='text-align: center; font-size: 36px;'>🤼️‍♂️ Gymshark AI Assistant</h1>
""", unsafe_allow_html=True)

# ---- SESSION STATE ----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "transcribed_input" not in st.session_state:
    st.session_state.transcribed_input = ""
if "last_voice_input" not in st.session_state:
    st.session_state.last_voice_input = ""

# ---- CHAT DISPLAY ----
st.subheader("🕡️ Conversation")
chat_container = st.container()
with chat_container:
    for speaker, message in st.session_state.chat_history:
        st.markdown(f"**{speaker}:**", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 18px; margin-bottom: 0.5rem;'>{message}</div>", unsafe_allow_html=True)

        # Inject text-to-speech for the most recent AI message
        if speaker == "🧫 AI" and message == st.session_state.chat_history[-1][1]:
            components.html(
                f"""
                <button onclick="const utterance = new SpeechSynthesisUtterance(`{message}`); window.speechSynthesis.speak(utterance);"
                        style="margin-top:5px;padding:8px 14px;font-size:14px;border:none;border-radius:8px;background:#444;color:white;cursor:pointer;">
                    🔊 Read Aloud
                </button>
                """,
                height=50
            )
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
            submitted = st.form_submit_button("📃 Ask")

            if submitted and user_question.strip():
                with st.spinner("Thinking..."):
                    try:
                        res = requests.post(backend_url, json={"username": "guest", "question": user_question})
                        answer = res.json().get("answer", "No answer received.")
                        st.session_state.chat_history.append(("🧑 You", user_question))
                        st.session_state.chat_history.append(("🧫 AI", answer))
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
                    st.session_state.chat_history.append(("🧫 AI", answer))
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
