import streamlit as st
import google.generativeai as genai
import os
import time
from google.api_core.exceptions import InternalServerError

load_dotenv()
# Configure the Generative AI API
genai.configure(api_key=os.getenv('api_key'))

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

st.title('Chatbot Assistant')

user_input = st.text_input('Ask me anything:')
if user_input:
    try:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = chat.send_message(user_input)
                st.markdown(response.text)
                break
            except InternalServerError as e:
                if attempt < max_retries - 1:
                    st.warning("Encountered an error, retrying...")
                    time.sleep(2)
                else:
                    st.error("The server is currently unavailable. Please try again later.")
                    st.text("Error details have been logged.")
                    break
    except Exception as e:
        st.error("An unexpected error occurred. Please try again.")
        st.text(f"Error: {str(e)}")
else:
    st.text('Please enter a question.')
