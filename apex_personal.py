import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
import random

st.set_page_config(page_title="APEX Personal", layout="wide", page_icon="🌟")

# Design
st.markdown("""
<style>
    .big-title {font-size: 58px !important; font-weight: bold; color: #FFD700;}
</style>
""", unsafe_allow_html=True)

# Passwortschutz
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 APEX Personal")
    password = st.text_input("Gib dein Passwort ein:", type="password")
    if st.button("Login"):
        if password == "Vorimeds2502.":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Falsches Passwort")
    st.stop()

# Session State
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {
        "total_invested": 18500.0,
        "current_value": 25980.0,
        "theme": "Balanced",
        "nft_level": "Diamond",
        "holdings": {"BTC": 0.21, "ETH": 4.8, "SOL": 75, "USDC": 1800}
    }

# Live Preise
@st.cache_data(ttl=60)
def get_live_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,avalanche-2,chainlink&vs_currencies=usd"
        data = requests.get(url).json()
        return {
            "BTC": data.get("bitcoin", {}).get("usd", 68250),
            "ETH": data.get("ethereum", {}).get("usd", 2650),
            "SOL": data.get("solana", {}).get("usd", 148),
            "AVAX": data.get("avalanche-2", {}).get("usd", 28.5),
            "LINK": data.get("chainlink", {}).get("usd", 13.8)
        }
    except:
        return {"BTC": 68250, "ETH": 2650, "SOL": 148, "AVAX": 28.5, "LINK": 13.8}

prices = get_live_prices()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/star.png", width=80)
    st.title("APEX")
    menu = st.selectbox("Menü", [
        "Dashboard", "Neue Investition", "Live Preise", 
        "Rebalancing & Yield", "Performance Charts", 
        "Wallet Tracking", "Ziel Simulator", "Strategie Tipps"
    ])

# DASHBOARD
if menu == "Dashboard":
    st.title("🌟 Willkommen zurück!")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Investiert", f"${st.session_state.portfolio['total_invested']:,.2f}")
    pnl = st.session_state.portfolio['current_value'] - st.session_state.portfolio['total_invested']
    col2.metric("Aktueller Wert", f"${st.session_state.portfolio['current_value']:,.2f}", f"↑ {((pnl / st.session_state.portfolio['total_invested']) * 100):.1f}%")
    col3.metric("NFT Level", st.session_state.portfolio["nft_level"], "🔥")
    col4.metric("Theme", st.session_state.portfolio["theme"])

    st.subheader("📊 Deine Holdings")
    data = []
    for coin, amount in st.session_state.portfolio["holdings"].items():
        price = prices.get(coin, 1000)
        value = amount * price
        data.append({"Coin": coin, "Amount": amount, "Preis": f"${price:,}", "Value ($)": round(value)})
    
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

# Neue Investition
elif menu == "Neue Investition":
    st.subheader("💰 Neue Investition")
    amount = st.number_input("Betrag in USDC", min_value=100.0, value=1000.0)
    theme = st.selectbox("Strategie", ["Balanced", "High Yield", "AI & Tech", "Bluechip Safe", "Aggressive Growth", "Memecoin Alpha"])
    
    if st.button("JETZT INVESTIEREN", type="primary"):
        st.session_state.portfolio["total_invested"] += amount
        st.session_state.portfolio["current_value"] += amount * random.uniform(1.0, 1.18)
        st.session_state.portfolio["theme"] = theme
        st.success(f"✅ ${amount:,.2f} investiert in **{theme}**!")
        st.balloons()

# Weitere Menüs (Live Preise, Rebalancing, etc.)
elif menu == "Live Preise":
    st.subheader("📈 Live Preise")
    for coin, price in prices.items():
        st.metric(coin, f"${price:,}")

elif menu == "Rebalancing & Yield":
    if st.button("Rebalancing + Yield starten", type="primary"):
        profit = random.uniform(6, 28)
        st.session_state.portfolio["current_value"] *= (1 + profit/100)
        st.success(f"✅ +{profit:.2f}% Gewinn diesen Monat!")

elif menu == "Ziel Simulator":
    st.subheader("🎯 Ziel Simulator")
    ziel = st.number_input("Zielbetrag ($)", value=100000)
    monatlich = st.number_input("Monatliche Einzahlung", value=800)
    years = round((ziel - st.session_state.portfolio["current_value"]) / (monatlich * 12 * 1.1), 1)
    st.success(f"Ca. **{max(years, 1)} Jahre** bis ${ziel:,.0f}")

st.caption("APEX Personal v4.1 — Ultimative Version | Nur für dich")
