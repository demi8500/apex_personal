# app.py - APEX Personal (minimal, fehlerfrei)
# Passwort: bnc2500
# Benötigt: streamlit, requests, pandas
# Install: python -m pip install streamlit requests pandas

import io
import time
import requests
import streamlit as st
import pandas as pd

st.set_page_config("APEX Personal", layout="wide")

# Minimal CSS (optional)
st.markdown(
    """
    <style>
    .block-container { background-color: #0b1020; color: #d6e1ff; }
    .stButton>button { background-color:#0f62fe;color:white; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Coins
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

# Session defaults
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "holdings" not in st.session_state:
    st.session_state.holdings = {"BTC": 0.01, "ETH": 0.1}
if "price_cache" not in st.session_state:
    st.session_state.price_cache = {}
if "price_ts" not in st.session_state:
    st.session_state.price_ts = 0.0

# Auth
def login():
    st.title("APEX Personal — Login")
    pwd = st.text_input("Passwort", type="password")
    if st.button("Anmelden"):
        if pwd == "bnc2500":
            st.session_state.authenticated = True
            try:
                st.experimental_rerun()
            except Exception:
                pass
        else:
            st.error("Falsches Passwort")

if not st.session_state.authenticated:
    login()
    st.stop()

# Price fetch with simple caching
def fetch_prices(symbols):
    now = time.time()
    if now - st.session_state.price_ts < 30 and st.session_state.price_cache:
        return st.session_state.price_cache
    ids = ",".join(COINS[s] for s in symbols)
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ids, "vs_currencies": "usd", "include_24hr_change": "true"}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        out = {}
        for s in symbols:
            cid = COINS[s]
            entry = data.get(cid, {})
            out[s] = {"price": entry.get("usd"), "change_24h": entry.get("usd_24h_change")}
        st.session_state.price_cache = out
        st.session_state.price_ts = now
        return out
    except Exception:
        if st.session_state.price_cache:
            return st.session_state.price_cache
        return {s: {"price": None, "change_24h": None} for s in symbols}

# Helpers
def portfolio_df(holdings, prices):
    rows = []
    for coin, amt in holdings.items():
        info = prices.get(coin, {})
        p = info.get("price")
        val = p * amt if p is no
