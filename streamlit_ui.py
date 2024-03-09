import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

PROMPT = """
SYSTEM MESSAGE: You are a chatbot designed to assist users with their queries about the weather in different cities around the world. User will ask you about this information. Your job is to help them.
START OF CHAT: Now introduce yourself.
"""

# Initialize Gemini-Pro 
load_dotenv(find_dotenv())
genai.configure()
model = genai.GenerativeModel('gemini-1.0-pro-latest')

# Gemini uses 'model' for assistant; Streamlit uses 'assistant'
def role_to_streamlit(role):
  if role == "model":
    return "assistant"
  else:
    return role

# Add a Gemini Chat history object to Streamlit session state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history = [])
    st.session_state.chat.send_message(PROMPT)

# Display Form Title
st.title("Chat with Google Gemini-Pro!")

# Display chat messages from history above current input box
for message in st.session_state.chat.history[1:]:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Accept user's next message, add to context, resubmit context to Gemini
if prompt := st.chat_input("I possess a well of knowledge. What would you like to know?"):
    # Display user's last message
    st.chat_message("user").markdown(prompt)
    
    # Send user entry to Gemini and read the response
    response = st.session_state.chat.send_message(prompt)
    
    # Display last 
    with st.chat_message("assistant"):
        st.markdown(response.text)