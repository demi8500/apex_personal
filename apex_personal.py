# apex_personal.py
# APEX Personal - Single-file Streamlit app
# Requirements:
# - Passwortschutz (Passwort: "bnc2500")
# - Dunkles modernes Design
# - Sidebar Menü: Dashboard, Trading Signals, Holdings bearbeiten, Neue Investition, Live Preise, Ziel Simulator
# - CoinGecko API für Live-Preise
# - Lokale Speicherung der Holdings in holdings.json
# - Sauber, verständlich kommentiert

import streamlit as st
import requests
import json
import os
from datetime import datetime
from math import log, ceil

# --------------------
# Konfiguration
# --------------------
APP_TITLE = "APEX Personal"
PASSWORD = "bnc2500"
HOLDINGS_FILE = "holdings.json"
COINS = [
    "bitcoin", "ethereum", "solana", "binancecoin", "ripple",  # BTC, ETH, SOL, BNB, XRP
    "dogecoin", "shiba-inu", "pepe", "bonk", "wif", "floki",   # DOGE, SHIB, PEPE, BONK, WIF, FLOKI
    "cardano", "avalanche-2", "chainlink", "toncoin"           # ADA, AVAX, LINK, TON
]
# Kurzbezeichnungen (für Anzeige)
COIN_SYMBOLS = {
    "bitcoin": "BTC", "ethereum": "ETH", "solana": "SOL", "binancecoin": "BNB", "ripple": "XRP",
    "dogecoin": "DOGE", "shiba-inu": "SHIB", "pepe": "PEPE", "bonk": "BONK", "wif": "WIF", "floki": "FLOKI",
    "cardano": "ADA", "avalanche-2": "AVAX", "chainlink": "LINK", "toncoin": "TON"
}
VS_CURRENCY = "usd"  # Preise in USD

# --------------------
# Hilfsfunktionen
# --------------------

def init_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "holdings" not in st.session_state:
        st.session_state.holdings = load_holdings()
    if "prices" not in st.session_state:
        st.session_state.prices = {}

def load_holdings():
    # Lade Holdings von Datei oder initialisiere leere Struktur (alle Coins mit 0)
    if os.path.exists(HOLDINGS_FILE):
        try:
            with open(HOLDINGS_FILE, "r") as f:
                data = json.load(f)
            # Sicherstellen, dass alle Coins vorhanden sind
            for c in COINS:
                if c not in data:
                    data[c] = 0.0
            return data
        except Exception:
            pass
    # Standard: alle 0
    return {c: 0.0 for c in COINS}

def save_holdings():
    try:
        with open(HOLDINGS_FILE, "w") as f:
            json.dump(st.session_state.holdings, f, indent=2)
    except Exception as e:
        st.error(f"Fehler beim Speichern: {e}")

def fetch_prices(ids):
    # CoinGecko simple price endpoint
    ids_str = ",".join(ids)
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ids_str, "vs_currencies": VS_CURRENCY, "include_24hr_change": "true"}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        # Ensure keys exist for all ids
        prices = {}
        for cid in ids:
            if cid in data:
                prices[cid] = {
                    "price": data[cid].get(VS_CURRENCY, None),
                    "change_24h": data[cid].get(f"{VS_CURRENCY}_24h_change", 0.0)
                }
            else:
                prices[cid] = {"price": None, "change_24h": 0.0}
        return prices
    except Exception as e:
        st.error(f"Fehler beim Abrufen der Preise: {e}")
        return {cid: {"price": None, "change_24h": 0.0} for cid in ids}

def compute_portfolio_value(holdings, prices):
    total = 0.0
    per_coin = {}
    for c, amt in holdings.items():
        price = prices.get(c, {}).get("price")
        value = (price or 0.0) * amt
        per_coin[c] = {"amount": amt, "price": price or 0.0, "value": value}
        total += value
    return total, per_coin

def signal_from_change(change_pct):
    # Einfache Signallogik basierend auf 24h Veränderung
    # thresholds (kann angepasst werden)
    if change_pct is None:
        return "HOLD"
    if change_pct >= 10:
        return "STRONG BUY"
    if change_pct >= 2:
        return "BUY"
    if change_pct <= -10:
        return "STRONG SELL"
    if change_pct <= -2:
        return "SELL"
    return "HOLD"

def years_to_target(current, monthly, target, annual_return=0.12):
    # Berechne Jahre bis Ziel mit monatlichen Einzahlungen und angenommener jährlicher Rendite
    # Formel: Future value of a series + current growth. Iterative simulate if needed.
    if monthly <= 0 and current <= 0:
        return float("inf")
    r_month = (1 + annual_return) ** (1/12) - 1
    fv_current = current
    months = 0
    # safety cap
    while fv_current < target and months < 1000:
        # monthly contribution at start of period
        fv_current = fv_current * (1 + r_month) + monthly
        months += 1
    return months / 12.0 if months < 1000 else float("inf")

# --------------------
# UI: Theme / Layout
# --------------------
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")
# Minimaler Dark Style über CSS
st.markdown(
    """
    <style>
    /* dunkles Farbschema */
    .stApp { background-color: #0f1720; color: #e6eef8; }
    .css-1d391kg { color: #
