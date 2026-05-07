# APEX Personal - Single-file Streamlit App
# Datum (für Referenz): 05/07/2026
# Beschreibung: Portfolio-Tool mit Passwortschutz, CoinGecko-Preisen, Signals, Holdings-Management, Simulator.
# Passwort: "bnc2500"
#
# Hinweise:
# - Einfacher Passwortschutz (nur für Demo). In Produktion bitte sichere Auth/HTTPS verwenden.
# - Holdings werden in st.session_state gespeichert und optional lokal in "holdings.json".
# - Benötigte Bibliotheken: streamlit, requests, pandas, numpy
#   Install: pip install streamlit requests pandas numpy

import streamlit as st
import requests
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

# ---------------------------
# Konfiguration
# ---------------------------
st.set_page_config(page_title="APEX Personal", layout="wide", initial_sidebar_state="expanded")
PASSWORD = "bnc2500"
HOLDINGS_FILE = "holdings.json"  # optional persistence
COINS = ["bitcoin", "ethereum", "solana", "binancecoin", "ripple", "dogecoin",
         "shiba-inu", "pepe", "bonk", "wif", "floki", "cardano", "avalanche-2",
         "chainlink", "toncoin"]
# Display names mapping (CoinGecko id -> ticker/pretty)
DISPLAY = {
    "bitcoin": "BTC", "ethereum": "ETH", "solana": "SOL", "binancecoin": "BNB",
    "ripple": "XRP", "dogecoin": "DOGE", "shiba-inu": "SHIB", "pepe": "PEPE",
    "bonk": "BONK", "wif": "WIF", "floki": "FLOKI", "cardano": "ADA",
    "avalanche-2": "AVAX", "chainlink": "LINK", "toncoin": "TON"
}
COINGECKO_API = "https://api.coingecko.com/api/v3"

# ---------------------------
# Styling (dunkles, modernes Design)
# ---------------------------
st.markdown(
    """
    <style>
    /* Hintergrund dunkel */
    .stApp {
        background-color: #0f1720;
        color: #e6eef8;
    }
    /* Sidebar style */
    .css-1d391kg { background-color: #0b1220 !important; }
    .css-1y4p8pa { background-color: #0b1220 !important; }
    /* Karten/Boxes */
    .card {
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border-radius: 8px;
        padding: 12px;
    }
    /* Tabellen */
    .stDataFrame table { color: #e6eef8; }
    /* Inputs text color */
    input, textarea { color: #e6eef8; background: #07101a !important; }
    </style>
    """,
    unsafe_allow_html=Tr
