import streamlit as st
import pandas as pd
import requests
import random

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

st.title("🌟 APEX Personal")
st.subheader("Major Coins + Memecoins")

coins = ["BTC", "ETH", "SOL", "BNB", "XRP", "DOGE", "SHIB", "PEPE", "BONK", "WIF", "FLOKI", "ADA", "AVAX", "LINK", "TON"]

if "my_holdings" not in st.session_state:
    st.session_state.my_holdings = {coin: 0.0 for coin in coins}

@st.cache_data(ttl=30)
def get_prices():
    try:
        ids = "bitcoin,ethereum,solana,binancecoin,ripple,dogecoin,shiba-inu,pepe,bonk,dogwifhat,floki,cardano,avalanche-2,chainlink,toncoin"
        r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd")
        return r.json()
    except:
        return {}

prices = get_prices()

menu = st.sidebar.selectbox("Menü", ["Dashboard", "Trading Signals", "Holdings bearbeiten", "Neue Investition", "Live Preise"])

if menu == "Dashboard":
    total = 0.0
    data = []
    for coin, amount in st.session_state.my_holdings.items():
        if amount > 0:
            price = prices.get(coin.lower().replace("wif","dogwifhat").replace("shib","shiba-inu").replace("pepe","pepe").replace("bonk","bonk
