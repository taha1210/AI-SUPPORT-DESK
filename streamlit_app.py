import streamlit as st
import requests
import json

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="AI Support Desk", page_icon="🤖")
st.title("🤖 AI Support Desk")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    import uuid
    st.session_state.thread_id = str(uuid.uuid4()) 

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("How can I help you today?"):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        response_placeholder = st.empty() 
        full_response = ""
        
        payload = {
            "message": user_input, 
            "thread_id": st.session_state.thread_id
        }
        
        try:
            with requests.post(API_URL, json=payload, stream=True) as r:
                for line in r.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith("data: "):
                            data = json.loads(decoded_line[6:])
                            content = data.get("content", "")
                            
                            full_response = content 
                            response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
        
        except Exception as e:
            st.error(f"Error connecting to backend: {e}")
            full_response = "Sorry, I'm having trouble connecting to the server."

    st.session_state.messages.append({"role": "assistant", "content": full_response})