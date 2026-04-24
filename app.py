import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import pydeck as pdk
from bs4 import BeautifulSoup
import json

st.set_page_config(page_title="URP & Data AI", layout="wide")
st.title("📊 Advanced Geospatial & Data Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

def smart_render(text):
    # ১. ম্যাপ রেন্ডারিং
    if '"lat"' in text.lower() and '"lon"' in text.lower():
        try:
            data = json.loads(text)
            df = pd.DataFrame(data)
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(latitude=df['lat'].mean(), longitude=df['lon'].mean(), zoom=11, pitch=50),
                layers=[pdk.Layer('ScatterplotLayer', data=df, get_position='[lon, lat]', get_color='[200, 30, 0, 160]', get_radius=200)]
            ))
            return
        except: pass

    # ২. চার্ট রেন্ডারিং
    if text.startswith('[{') or text.startswith('{'):
        try:
            data = json.loads(text)
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                fig = px.bar(df, x=df.columns[0], y=numeric_cols[0], template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
            return
        except: pass

    # ৩. HTML ও Markdown রেন্ডারিং
    if bool(BeautifulSoup(text, "html.parser").find()):
        st.markdown(text, unsafe_allow_html=True)
    else:
        st.markdown(text)

# চ্যাট হিস্ট্রি
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        smart_render(message["content"])

# ইউজার ইনপুট ও এপিআই কল
if prompt := st.chat_input("Ask me about maps, charts or planning..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        webhook_url = "https://meheran.loseyourip.com/webhook/9664f55f-56d9-4b2f-ab20-faec93bb7f29"
        
        try:
            with st.spinner("Processing Data..."):
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
