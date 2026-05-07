import streamlit as st
import pandas as pd
import random

# Page configuration
st.set_page_config(
    page_title="APEX Personal",
    page_icon="📈",
    layout="wide"
)

# Main header
st.title("📈 APEX Personal - Crypto Trading Dashboard")

# Login section
with st.sidebar:
    st.header("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == "admin" and password == "password":
            st.success("✅ Login erfolgreich!")
        else:
            st.error("❌ Falsche Anmeldedaten!")

# Main content
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💰 Portfolio", "🎯 Signale"])

with tab1:
    st.header("Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("BTC", "$67,543", "2.4%")
    with col2:
        st.metric("ETH", "$3,234", "1.8%")
    with col3:
        st.metric("SOL", "$156", "5.2%")
    with col4:
