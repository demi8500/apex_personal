# app.py - APEX Personal (funktionierende Single-File Streamlit-App)
# Passwort: bnc2500
# Benötigt: streamlit, requests, pandas, numpy, plotly
# Install: python -m pip install --upgrade pip
#         python -m pip install streamlit requests pandas numpy plotly

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
    input, select, textarea { background-color: #0f1724 !important; color: #d6e1ff !important; border: 1px solid #223 !important; }
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
# Robust price fetch with caching/backoff
# ---------------------
def fetch_prices(symbols, max_retries=5, cache_ttl=30):
    """
    Robust price fetch with exponential backoff and caching.
    Returns dict: symbol -> {"price":..., "change_24h":...}
    """
    now = time.time()
    # Use cached if fresh
    if now - st.session_state.get("prices_timestamp", 0) < cache_ttl and st.session_state.get("last_prices"):
        return st.session_state["last_prices"]

    ids = ",".join(COINS[s] for s in symbols)
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ids, "vs_currencies": "usd", "include_24hr_change": "true"}

    attempt = 0
    while attempt <= max_retries:
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            out = {}
            for s in symbols:
                cid = COINS[s]
                entry = data.get(cid, {})
                out[s] = {"price": entry.get("usd"), "change_24h": entry.get("usd_24h_change")}
            # Cache results
            st.session_state["last_prices"] = out
            st.session_state["prices_timestamp"] = time.time()
            return out
        except requests.HTTPError as e:
            status = getattr(e.response, "status_code", None)
            if status == 429:
                wait = min(60, (2 ** attempt))
            else:
                wait = (2 ** attempt) * 0.5
            attempt += 1
            time.sleep(wait)
        except Exception:
            attempt += 1
            time.sleep(min(5, 0.5 * (2 ** attempt)))

    # Fallback: return last known prices or None-values
    if st.session_state.get("last_prices"):
        return st.session_state["last_prices"]
    r
