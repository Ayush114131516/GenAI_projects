import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-pro")
chat=model.start_chat(history=[])

def get_reponse(question):
    response=chat.send_message(question,stream=True)
    return response

st.set_page_config(page_title="Q&A ChatBot")
st.header("LLM Q&A Application")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]

input=st.text_input("Input:",key="input")
submit=st.button("⬆️")

if submit and input:
    response=get_reponse(input)
    st.session_state['chat_history'].append(("👨🏻",input))
    st.subheader("Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state["chat_history"].append(("🤖",response))

st.subheader("Chat History:")
for role,text in st.session_state["chat_history"]:
    st.write(f"{role} : {text}")