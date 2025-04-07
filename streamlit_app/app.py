import streamlit as st
import requests

st.set_page_config(page_title="AI Sales Chatbot", page_icon="🍭")
backend_base = "https://321f-34-124-252-237.ngrok-free.app"
backend_url = backend_base + "/ask"

USERNAME = "user123"  # You can make this dynamic via login or input

st.title("🛍️ AI Sales Assistant")

# SESSION STATE
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# CLEAR BUTTON
if st.button("🔁 Clear Conversation"):
    st.session_state.chat_history = []
    st.session_state.input = ""
    try:
        requests.post(backend_base + "/clear", json={"username": USERNAME})
    except:
        st.warning("Failed to clear on server.")
    st.success("Conversation cleared!")
    st.rerun()

# DISPLAY CHAT
st.subheader("🗣️ Conversation")
for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")
st.divider()

# USER INPUT FORM
with st.form("user_input_form", clear_on_submit=True):
    user_question = st.text_input("Ask a product-related question:", value=st.session_state.user_input, key="input")
    submitted = st.form_submit_button("📤 Ask")

    if submitted and user_question.strip():
        with st.spinner("Thinking..."):
            try:
                res = requests.post(backend_url, json={"username": USERNAME, "question": user_question})
                answer = res.json().get("answer", "No answer received.")

                st.session_state.chat_history.append(("🧑 You", user_question))
                st.session_state.chat_history.append(("🤖 AI", answer))
                st.session_state.user_input = ""
                st.rerun()

            except Exception as e:
                st.error(f"\u274c Error: {e}")
    elif submitted:
        st.warning("Please enter a question.")
