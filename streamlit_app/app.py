# streamlit_app/app.py
import streamlit as st
import requests

st.set_page_config(page_title="AI Sales Chatbot")

st.title("🛍️ AI Sales Assistant")
user_question = st.text_input("Ask a product-related question:")

if st.button("Send"):
    if user_question.strip() != "":
        with st.spinner("Thinking..."):
            try:
                # Replace this URL with your ngrok URL from Google Colab
                backend_url = "https://8b5a-34-142-223-237.ngrok-free.app/ask"
                res = requests.post(backend_url, json={"question": user_question})
                data = res.json()
                st.success(data.get("answer", "No answer received."))
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question.")
