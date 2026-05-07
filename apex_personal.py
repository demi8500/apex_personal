# app.py - APEX Personal (korrigiert)
# Passwort: bnc2500
# Single-file Streamlit App mit:
# - Passwortschutz
# - Dark modern design
# - Sidebar Menü: Dashboard, Trading Signals, Holdings bearbeiten, Neue Investition, Live Preise, Ziel Simulator
# - Erweiterte Trading-Signale (24h-change + RSI)
# - Plotly Chart für Preisverlauf
# - CSV Import/Export für Holdings
# - CoinGecko für Preise & historische Daten

import streamlit as st
import requests
import pandas as pd
import numpy as np
import time
import math
import io
import plotly.express as px

st.set_page_config(page_title="APEX Personal", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.reportview-container, .main, .block-container { background-color: #0b1020; color: #d6e1ff; }
.stButton>button { background-color: #0f62fe; color: white; }
.stTextInput>div>div>input, .stNumberInput>div>div>input { background-color: #0f1724; color: #d6e1ff; border: 1px solid #223; }
.card { background: #0f1724; padding: 12px; border-radius: 10px; border: 1px solid #233; }
</style>
""", unsafe_allow_html=True)

# --------------------------
# Coin mapping (symbols -> CoinGecko id)
# --------------------------
COINS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "DOGE": "dogecoin",
    "SHIB": "shiba-inu",
    "PEPE": "pepe",
    "BONK": "bonk",
    "WIF": "wif",
    "FLOKI": "floki",
    "ADA": "cardano",
    "AVAX": "avalanche-2",
    "LINK": "chainlink",
    "TON": "toncoin",
}
COIN_SYMBOLS = list(COINS.keys())

# --------------------------
# Utilities: CoinGecko APIs
# --------------------------
def fetch_prices(symbols):
    ids = ",".join([COINS[s] for s in
