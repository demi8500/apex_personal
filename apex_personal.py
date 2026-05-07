# apex_personal.py
# APEX Personal - Single-file Streamlit app (final, with safe_rerun)
# Passwort: "bnc2500"
# Benötigt: streamlit, requests
# Installation: pip install streamlit requests
# Start: streamlit run apex_personal.py

import streamlit as st
import requests
import json
import os
from datetime import datetime
from math import inf

# --------------------
# Konfiguration
# --------------------
APP_TITLE = "APEX Personal"
PASSWORD = "bnc2500"
HOLDINGS_FILE = "holdings.json"
VS_CURRENCY = "usd"

COINS = [
    ("bitcoin", "BTC"),
    ("ethereum", "ETH"),
    ("solana", "SOL"),
    ("binancecoin", "BNB"),
    ("ripple", "XRP"),
    ("dogecoin", "DOGE"),
    ("shiba-inu", "SHIB"),
    ("pepe", "PEPE"),
    ("bonk", "BONK"),
    ("wif-token", "WIF"),
    ("floki", "FLOKI"),
    ("cardano", "ADA"),
    ("avalanche-2", "AVAX"),
    ("chainlink", "LINK"),
    ("toncoin", "TON"),
]

# --------------------
# Utilities
# --------------------

def safe_rerun():
    try:
        st.experimental_rerun()
    except Exception:
        # In some environments experimental_rerun may not be available; ignore silently.
        return

def debug(msg: str):
    if st.session_state.get("_debug_enabled", False):
        st.text(f"[DEBUG] {msg}")

def ensure_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "holdings" not in st.session_state:
        st.session_state.holdings = load_holdings()
    if "prices" not in st.session_state:
        st.session_state.prices = {}
    if "_debug_enabled" not in st.session_state:
        st.session_state._debug_enabled = False

def load_holdin
