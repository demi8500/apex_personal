import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
import random

st.set_page_config(page_title="APEX Personal", layout="wide", page_icon="🌟")

# Modernes Dark Design
st.markdown("""
<style>
    .big-title {font-size: 58px !important; font-weight: bold; color: #FFD700;}
    .metric-card {background-color: #1E1E1E; padding: 20px; border-radius: 12px; border: 1px solid #333;}
</style>
""", unsafe_allow_html=True)

# Passwortschutz
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 APEX Personal")
    password = st.text_input("Gib dein Passwort ein:", type="password")
    if st.button("Login"):
        if password == "apex2026":  # Du kannst das Passwort später ändern
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Falsches Passwort")
    st.stop()

# ==================== SESSION STATE ====================
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {
        "total_invested": 18500.0,
        "current_value": 25980.0,
        "theme": "Balanced",
        "nft_level": "Diamond",
        "holdings": {"BTC": 0.21, "ETH": 4.8, "SOL": 75, "USDC": 1800}
    }

# Live Preise (CoinGecko)
@st.cache_data(ttl=60)
def get_live_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,avalanche-2,chainlink&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return {
            "BTC": data["bitcoin"]["usd"],
            "ETH": data["ethereum"]["usd"],
            "SOL": data["solana"]["usd"],
            "AVAX": data["avalanche-2"]["usd"],
            "LINK": data["chainlink"]["usd"]
        }
    except:
        return {"BTC": 68250, "ETH": 2650, "SOL": 148, "AVAX": 28.5, "LINK": 13.8}

prices = get_live_prices()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/star.png", width=80)
    st.title("APEX")
    menu = st.selectbox("Menü", [
        "Dashboard", "Neue Investition", "Portfolio Themes", 
        "Rebalancing & Yield", "Live Preise", "Performance Charts",
        "Wallet Tracking", "Ziel Simulator", "Strategie Tipps"
    ])

# ==================== DASHBOARD ====================
if menu == "Dashboard":
    st.title("🌟 Willkommen zurück!")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Investiert", f"${st.session_state.portfolio['total_invested']:,.2f}")
    pnl = st.session_state.portfolio['current_value'] - st.session_state.portfolio['total_invested']
    col2.metric("Aktueller Wert", f"${st.session_state.portfolio['current_value']:,.2f}", f"↑ {((pnl / st.session_state.portfolio['total_invested']) * 100):.1f}%")
    col3.metric("NFT Level", st.session_state.portfolio["nft_level"], "🔥")
    col4.metric("Theme", st.session_state.portfolio["theme"])

    st.subheader("📊 Deine Holdings")
    holdings_data = {"Coin": [], "Amount": [], "Value ($)": []}
    for coin, amount in st.session_state.portfolio["holdings"].items():
        value = amount * prices.get(coin, 1000)
        holdings
