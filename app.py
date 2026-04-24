import streamlit as st
import requests

st.set_page_config(page_title="AI Assistant", layout="centered")
st.title("🤖 My Custom AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

   with st.chat_message("assistant"):
    webhook_url = "https://n8n.your-digitalocean-domain.com/webhook/streamlit-chat"
    
    try:
        # n8n এ ডাটা পাঠানো হচ্ছে
        response = requests.post(webhook_url, json={"chatInput": prompt})
        
        # ডাটা ঠিকমতো আসলে সেটি দেখানো হচ্ছে
        if response.status_code == 200:
            res_data = response.json()
            # n8n এর Respond to Webhook নোড থেকে আসা 'output'
            full_response = res_data.get("output", "No reply received.")
            
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            st.error(f"Error: Server returned status {response.status_code}")
            
    except Exception as e:
        st.error(f"Something went wrong: {e}")
