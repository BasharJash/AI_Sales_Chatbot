import streamlit as st
import requests
import pyttsx3

# ---- CONFIG ----
st.set_page_config(page_title="AI Sales Chatbot", page_icon="🛍️")
backend_url = "https://613c-34-143-231-179.ngrok-free.app/ask"  # ✅ Replace with actual

st.title("🛍️ AI Sales Assistant")

# ---- SESSION STATE ----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---- CLEAR BUTTON ----
if st.button("🔁 Clear Conversation"):
    st.session_state.chat_history = []
    st.success("Conversation cleared!")

# ---- USER INPUT ----
user_question = st.text_input("Ask a product-related question:")

if st.button("📤 Ask"):
    if user_question.strip():
        with st.spinner("Thinking..."):
            try:
                # Send question to backend
                res = requests.post(backend_url, json={"question": user_question})
                answer = res.json().get("answer", "No answer received.")

                # Save conversation
                st.session_state.chat_history.append(("🧑 You", user_question))
                st.session_state.chat_history.append(("🤖 AI", answer))

                # Voice output (optional)
                engine = pyttsx3.init()
                engine.say(answer)
                engine.runAndWait()

            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("Please enter a question.")

# ---- DISPLAY CHAT ----
st.divider()
st.subheader("🗣️ Conversation")
for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")
