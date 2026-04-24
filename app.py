import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
import plotly.express as px
import plotly.graph_objects as go
import json

# পেজ কনফিগারেশন
st.set_page_config(page_title="Data Scientist Bot", page_icon="📊", layout="wide")

st.title("📊 Advanced Analytics & Chat Interface")

if "messages" not in st.session_state:
    st.session_state.messages = []

# অ্যাডভান্সড রেন্ডারার ফাংশন
def smart_render(text):
    # ১. চেক করা হচ্ছে এটি কি কোনো JSON ডাটা কি না (চার্ট তৈরির জন্য)
    try:
        if text.startswith('{') or text.startswith('['):
            data = json.loads(text)
            df = pd.DataFrame(data)
            
            # টেবিল দেখানো
            st.subheader("Data Preview")
            st.dataframe(df, use_container_width=True)
            
            # অটোমেটিক চার্ট (যদি ডাটা সংখ্যাবাচক হয়)
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                st.subheader("Visualisation")
                fig = px.bar(df, x=df.columns[0], y=numeric_cols[0], title="Auto-generated Analysis")
                st.plotly_chart(fig, use_container_width=True)
            return
    except:
        pass

    # ২. HTML রেন্ডারিং
    if bool(BeautifulSoup(text, "html.parser").find()):
        st.markdown(text, unsafe_allow_html=True)
    # ৩. স্ট্যান্ডার্ড মার্কডাউন (টেবিল, বোল্ড, কোড ব্লক সব সহ)
    else:
        st.markdown(text)

# চ্যাট হিস্ট্রি
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        smart_render(message["content"])

# ইনপুট সেকশন
if prompt := st.chat_input("Ask about data, maps or urban planning..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

   if prompt := st.chat_input("Ask me about maps, charts or planning..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # আপনার প্রোডাকশন URL
        webhook_url = "https://meheran.loseyourip.com/webhook/9664f55f-56d9-4b2f-ab20-faec93bb7f29"
        
        try:
            with st.spinner("Processing Data..."):
                # এখানে ইনডেন্টেশন (স্পেস) একদম ঠিক করা আছে
                headers = {"Bypass-Tunnel-Reminder": "true", "User-Agent": "Mozilla/5.0"}
                response = requests.post(webhook_url, json={"chatInput": prompt}, headers=headers, timeout=1200)
            
            if response.status_code == 200:
                res_data = response.json()
                full_response = res_data.get("output", res_data.get("finalReply", "No response."))
                smart_render(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error(f"Server Error: {response.status_code} - Could not connect.")
                
        except Exception as e:
            st.error(f"Error: {e}")
