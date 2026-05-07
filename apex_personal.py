# app.py - APEX Personal (final corrected single-file)
# Passwort: bnc2500
# Benötigt: streamlit, requests, pandas, numpy, plotly
# Install: pip install streamlit requests pandas numpy plotly

import io
import math
import time
import requests
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="APEX Personal", layout="wide")

# ---------------------
# Styling (dark)
# ---------------------
st.markdown(
    """
    <style>
    .reportview-container, .main, .block-container { background-color: #0b1020; color: #d6e1ff; }
    .stButton>button { background-color: #0f62fe; color: white; }
    .stTextInput input, .stNumberInput input, .stSelectbox select { background-color: #0f1724; color: #d6e1ff; border: 1px solid #223; }
    .card { background: #0f1724; padding: 12px; border-radius: 10px; border: 1px solid #233; margin-bottom:12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------
# Coin definitions
# ---------------------
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

# ---------------------
# Utilities: CoinGecko
# ---------------------
def fetch_prices(symbols):
    ids = ",".join(COINS[s] for s in symbols)
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ids, "vs_currencies": "usd", "include_24hr_change": "true"}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    out = {}
    for s in symbols:
        cid = COINS[s]
        entry = data.get(cid, {})
        out[s] = {"price": entry.get("usd"), "change_24h": entry.get("usd_24h_change")}
    return out

def fetch_market_chart(symbol, days=90):
  
