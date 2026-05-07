# app.py - APEX Personal (minimal, fehlerfrei)
# Passwort: bnc2500
# Benötigt: streamlit, requests, pandas

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
    st.session_state["authenticated"] = False
if "holdings" not in st.session_state:
    st.session_state["holdings"] = {"BTC": 0.01, "ETH": 0.1}
if "price_cache" not in st.session_state:
    st.session_state["price_cache"] = {}
if "price_ts" not in st.session_state:
    st.session_state["price_ts"] = 0.0

# Auth
def login():
    st.title("APEX Personal — Login")
    pwd = st.text_input("Passwort", type="password", key="login_pwd")
    if st.button("Anmelden"):
        if pwd == "bnc2500":
            st.session_state["authenticated"] = True
            try
