import streamlit as st
import pandas as pd
import requests
import random
from datetime import datetime

st.set_page_config(page_title="APEX Personal", layout="wide", page_icon="🌟")

# Passwort
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 APEX Personal")
    pw = st.text_input("Passwort eingeben", type="password")
    if st.button("Login"):
        if pw == "bnc2500":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Falsches Passwort")
    st.stop()

st.title("🌟 APEX Personal v6.1")
st.subheader("Trading Signals + Portfolio Manager")

# Live Preise
@st.cache_data(ttl=30)
def get_prices():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,avalanche-2,chainlink,cardano&vs_currencies=usd")
        return r.json()
    except:
        return {}

prices = get_prices()

# Portfolio
if "my_holdings" not in st.session_state:
    st.session_state.my_holdings = {"BTC": 0.0, "ETH": 0.0, "SOL": 0.0, "AVAX": 0.0, "LINK": 0.0, "ADA": 0.0}

menu = st.sidebar.selectbox("Menü", ["Dashboard", "Trading Signals", "Holdings bearbeiten", "Neue Investition", "Live Preise", "Ziel Simulator"])

if menu == "Trading Signals":
    st.subheader("🔥 APEX Trading Signals")
    st.warning("⚠️ Dies sind **nur simulierte Signale** zu Bildungszwecken. Keine Finanzberatung!")

    for coin in ["BTC", "ETH", "SOL", "AVAX", "LINK"]:
        price = prices.get(coin.lower(), {}).get("usd", 1000)
        signal = random.choice(["STRONG BUY", "BUY", "HOLD", "SELL", "STRONG SELL"])
        strength = random.randint(60, 95)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col1:
            st.metric(coin, f"${price:,.2f}")
        with col2:
            if "BUY" in signal:
                st.success(f"**{signal}**")
            elif "SELL" in signal:
                st.error(f"**{signal}**")
            else:
                st.warning(f"**{signal}**")
        with col3:
            st.progress(strength / 100)
            st.caption(f"Stärke: {strength}%")

    st.info("Tipp: Kaufe bei **STRONG BUY**, verkaufe bei **STRONG SELL**. Immer mit Risikomanagement arbeiten!")

# Dashboard & andere Menüs (wie vorher)
elif menu == "Dashboard":
    # ... (früherer Code)
    st.write("Dashboard - deine echten Holdings")

# Rest der Menüs (Holdings bearbeiten, etc.) bleiben gleich wie vorher

st.caption("APEX Personal v6.1 – Mit Trading Signals | Nur für dich")
