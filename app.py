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

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def login_page():
    st.markdown('<div class="main-header">🔐 APEX Personal Login</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Geben Sie Ihren Benutzernamen ein")
            password = st.text_input("Password", type="password", placeholder="Geben Sie Ihr Passwort ein")
            login_button = st.form_submit
