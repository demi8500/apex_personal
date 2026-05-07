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

# Custom CSS for dark theme
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
    .signal-strong-sell {
        background: linear-gradient(135deg, #d32f2f, #b71c1c);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Coin mapping
COINS = ['BTC', 'ETH', 'SOL', 'BNB', 'XRP', 'DOGE', 'SHIB', 'PEPE', 'BONK', 'WIF', 'FLOKI', 'ADA', 'AVAX', 'LINK', 'TON']

COIN_MAPPING = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum', 
    'SOL': 'solana',
    'BNB': 'binancecoin',
    'XRP': 'ripple',
    'DOGE': 'dogecoin',
    'SHIB': 'shiba-inu',
    'PEPE': 'pepe',
    'BONK': 'bonk',
    'WIF': 'dogwifcoin',
    'FLOKI': 'floki',
    'ADA': 'cardano',
    'AVAX': 'avalanche-2',
    'LINK': 'chainlink',
    'TON': 'the
