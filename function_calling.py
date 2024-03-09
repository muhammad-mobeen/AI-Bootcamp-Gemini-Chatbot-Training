import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
import requests

PROMPT = """
SYSTEM MESSAGE: You are a chatbot designed to assist users with their queries about the weather in different cities around the world. User will ask you about this information. Your job is to help them.
START OF CHAT: Now introduce yourself.
"""

r_PROMPT = """
Your task is to extract a parameter from USER INPUT. User will ask you about the weather of a certain city. You have to identify the city name and respond only with that city name.
USER INPUT: {}
"""

# Initialize Gemini-Pro 
load_dotenv(find_dotenv())
genai.configure()
model = genai.GenerativeModel('gemini-1.0-pro-latest')


from bs4 import BeautifulSoup

def get_weather(city):
    # Creating url and requests instance
    url = "https://www.google.com/search?q="+"weather "+city
    html = requests.get(url).content
    # Getting raw data
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    data_str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    # Formatting data
    data = data_str.split('\n')
    time = data[0]
    sky = data[1]
    # Getting all div tags
    listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
    detailed_data = listdiv[5].text
    # Getting other required data
    pos = detailed_data.find('Wind')
    other_data = detailed_data[pos:]
    # Creating a dictionary to store the scraped data
    weather_data = {
        "Temperature": temp,
        "Time": time,
        "Sky Description": sky,
        "Other Details": other_data
    }
    return weather_data



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
st.title("Chat with Google Gemini-1.0-Pro!")

# Display chat messages from history above current input box
for message in st.session_state.chat.history[1:]:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Accept user's next message, add to context, resubmit context to Gemini
if prompt := st.chat_input("I possess a well of knowledge. What would you like to know?"):
    # Display user's last message
    st.chat_message("user").markdown(prompt)

    f_response = model.generate_content(r_PROMPT.format(prompt))
    print(f_response.text)
    ff_response = str(get_weather(f_response.text))
    print(ff_response)
    
    # Send user entry to Gemini and read the response
    response = st.session_state.chat.send_message(prompt+"\n\nRESPONSE FROM WEATHER STATION:\n"+ff_response)
    
    # Display last 
    with st.chat_message("assistant"):
        st.markdown(response.text)