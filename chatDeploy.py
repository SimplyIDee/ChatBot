import streamlit as st
import shelve
import warnings 
warnings.filterwarnings("ignore")
import google.generativeai as genai
from knowledge import googleModelKnowledge as myKnowledge

st.markdown("<h1 style='color: #780C28; font-size: 36px ; font-family: Tahoma; text-align: center;'>CHATBOT POWERED BY GEMINI</h1>", unsafe_allow_html = True)

st.markdown("<h3 style='margin-top: -20px; color: #1D1616; font-size: 24px ; font-family: Brush Script; text-align: center;'>Built by Lazy IDee</h3>", unsafe_allow_html = True)

st.markdown('<br><br>', unsafe_allow_html = True)


genai.configure(api_key = "AIzaSyCWcsJ08G5vPM7CfrcfEcQb6VYRSrlcYp8")

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 1024,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
 model_name="gemini-2.0-flash",
  generation_config=generation_config,
  system_instruction = myKnowledge()
)


def savedHistory(chatHistory, filename="chatHistory"):
  with shelve.open(filename) as db:
    db['chatHistory'] = chatHistory

def loadHistory(filename="chatHistory"):
  with shelve.open(filename) as db:
    return db.get('chatHistory', [])

history_ = loadHistory() 

chat_session = model.start_chat(
  history=history_
)

imageColumn, chatColumn = st.columns([2, 3])
with imageColumn:
    st.image("chatColumn.png", width = 300)

with chatColumn:
    userInput = st.chat_input("Say Something: ")
    if userInput:
        userOutput = st.chat_message(name='user')
        userOutput.write(userInput)
        response = chat_session.send_message(userInput)
        history_.append({"role": "user", "parts": [userInput]})
        history_.append({"role": "model", "parts": [response]})
        savedHistory(history_)
        
        modelOutput = st.chat_message(name='model') 
        modelOutput.write(response.text) 