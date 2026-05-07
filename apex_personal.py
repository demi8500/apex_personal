# apex_personal.py
# APEX Personal - überarbeitete Version mit Debugging-Output und verbesserter Fehlerbehandlung
# Passwort: "bnc2500"
# Single-file Streamlit App. Benötigt: streamlit, requests
# Install: pip install streamlit requests

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
# CoinGecko IDs und Symbole - entferne/ignoriere später ungültige IDs dynamisch
COINS = [
    ("bitcoin", "BTC"), ("ethereum", "ETH"), ("solana", "SOL"), ("binancecoin", "BNB"),
    ("ripple", "XRP"), ("dogecoin", "DOGE"), ("shiba-inu", "SHIB"), ("pepe", "PEPE"),
    ("bonk", "BONK"), ("wif-token", "WIF"), ("floki", "FLOKI"), ("cardano", "ADA"),
    ("avalanche-2", "AVAX"), ("chainlink", "LINK"), ("toncoin", "TON")
]
# Hinweis: einige IDs (z.B. wif-token) können anders heißen auf CoinGecko; app behandelt Missing gracefully.

# --------------------
# Hilfsfunktionen
# --------------------

def debug(msg):
    # Debug-Ausgabe in Streamlit App, nur sichtbar wenn Debug-Modus aktiviert
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

def load_holdings():
    # Lade Holdings von JSON oder initialisiere mit 0
    if os.path.exists(HOLDINGS_FILE):
        try:
            with open(HOLDINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # ensure all keys present
            out = {}
            for cid, sym in COINS:
                out[cid] = float(data.get(cid, 0.0))
            return out
        except Exception as e:
            # Wenn Laden fehlschlägt, logge Fehler und initialisiere neu
            print("Error loading holdings.json:", e)
    return {cid: 0.0 for cid, _ in COINS}

def save_holdings():
    try:
        with open(HOLDINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.holdings, f, indent=2)
        debug("Holdings saved to " + HOLDINGS_FILE)
