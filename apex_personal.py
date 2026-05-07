# APEX Personal - Single-file Streamlit App (fixed syntax)
# Date: 05/07/2026
# Passwort: "bnc2500"
# Benötigt: streamlit, requests, pandas, numpy

import streamlit as st
import requests
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

st.set_page_config(page_title="APEX Personal", layout="wide", initial_sidebar_state="expanded")

PASSWORD = "bnc2500"
HOLDINGS_FILE = "holdings.json"
COINS = ["bitcoin", "ethereum", "solana", "binancecoin", "ripple", "dogecoin",
         "shiba-inu", "pepe", "bonk", "wif", "floki", "cardano", "avalanche-2",
         "chainlink", "toncoin"]
DISPLAY = {
    "bitcoin": "BTC", "ethereum": "ETH", "solana": "SOL", "binancecoin": "BNB",
    "ripple": "XRP", "dogecoin": "DOGE", "shiba-inu": "SHIB", "pepe": "PEPE",
    "bonk": "BONK", "wif": "WIF", "floki": "FLOKI", "cardano": "ADA",
    "avalanche-2": "AVAX", "chainlink": "LINK", "toncoin": "TON"
}
COINGECKO_API = "https://api.coingecko.com/api/v3"

# Dark theme styling
st.markdown(
    """
    <style>
    .stApp { background-color: #0f1720; color: #e6eef8; }
    .css-1d391kg { background-color: #0b1220 !important; }
    .css-1y4p8pa { background-color: #0b1220 !important; }
    .card { background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
            border-radius: 8px; padding: 12px; margin-bottom: 12px; }
    .stDataFrame table { color: #e6eef8; }
    input, textarea { color: #e6eef8; background: #07101a !important; }
    </style>
    """,
    unsafe_allow_html=True
)

def load_holdings():
    if "holdings" not in st.session_state:
        holdings = {}
        if os.path.exists(HOLDINGS_FILE):
            try:
                with open(HOLDINGS_FILE, "r") as f:
                    data = json.load(f)
                holdings = {k: float(v) for k, v in data.items()}
            except Exception:
                holdings = {}
        for c in COINS:
            holdings.setdefault(c, 0.0)
        st.session_state["holdings"] = holdings
    return st.session_state["holdings"]

def save_holdings():
    try:
        with open(HOLDINGS_FILE, "w") as f:
            json.dump(st.session_state["holdings"], f)
    except Exception:
        pass

def fetch_prices(coin_ids):
    ids = ",".join(coin_ids)
    url = f"{C
