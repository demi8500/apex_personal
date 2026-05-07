# app.py - APEX Personal (final)
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
def fetch_market_chart(symbol, days=90):
    cid = COINS.get(symbol)
    if not cid:
        return pd.DataFrame(columns=["timestamp", "price"])
    url = f"https://api.coingecko.com/api/v3/coins/{cid}/market_chart"
    params = {"vs_currency": "usd", "days": days, "interval": "hourly" if days <= 90 else "daily"}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    prices = data.get("prices", [])
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

def fetch_market_chart(symbol, days=90):
    cid = COINS.get(symbol)
    if not cid:
        return pd.DataFrame(columns=["timestamp", "price"])
    url = f"https://api.coingecko.com/api/v3/coins/{cid}/market_ch
