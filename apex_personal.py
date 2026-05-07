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
if "authenticated" not
