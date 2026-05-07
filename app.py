import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
import random

# Page configuration
st.set_page_config(
    page_title="APEX Personal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00ff88;
        text-align: center;
        margin-bottom: 2rem;
    }
    .signal-strong-buy {
        background: linear-gradient(135deg, #00ff88, #00cc6a);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin: 0.5rem;
    }
    .signal-buy {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin: 0.5rem;
    }
    .signal-hold {
        background: linear-gradient(135deg, #FF9800, #F57C00);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin: 0.5rem;
    }
    .signal-sell {
        background: linear-gradient(135deg, #f44336, #d32f2f);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Main app
def main():
    st.markdown('<div class="main-header">📈 APEX Personal</div>', unsafe_allow_html=True)
    
    # Login form
    with st.sidebar:
        st.header("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if username == "admin" and password == "password":
                st.success("Login erfolgreich!")
            else:
                st.error("Falsche Anmeldedaten!")
    
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
            st.metric("Portfolio", "$15,430", "3.1%")
    
    with tab2:
        st.header("Portfolio Übersicht")
        
        portfolio_data = {
