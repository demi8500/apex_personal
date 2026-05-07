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

# Alle Coins (Major + Memecoins)
coins = ["BTC", "ETH", "SOL", "BNB", "XRP", "DOGE", "SHIB", "PEPE", "BONK", "WIF", "FLOKI", "BRETT", "POPCAT", "ADA", "AVAX", "LINK", "TON"]

# Live Preise
@st.cache_data(ttl=30)
def get_prices():
    try:
        ids = "bitcoin,ethereum,solana,binancecoin,ripple,dogecoin,shiba-inu,pepe,bonk,dogwifhat,floki,brett,popcat,cardano,avalanche-2,chainlink,toncoin"
        r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd")
        return r.json()
    except:
        return {}

prices = get_prices()

# Portfolio
if "my_holdings" not in st.session_state:
    st.session_state.my_holdings = {coin: 0.0 for coin in coins}

menu = st.sidebar.selectbox("Menü", ["Dashboard", "Trading Signals", "Holdings bearbeiten", "Neue Investition", "Live Preise"])

if menu == "Dashboard":
    total = 0.0
    data = []
    for coin, amount in st.session_state.my_holdings.items():
        if amount > 0:
            price = prices.get(coin.lower().replace("wif","dogwifhat").replace("shib","shiba-inu").replace("pepe","pepe").replace("bonk","bonk"), {}).get("usd", 0)
            value = amount * price
            total += value
            data.append({"Coin": coin, "Menge": amount, "Wert ($)": round(value, 2)})
    st.metric("Gesamtwert Portfolio", f"${total:,.2f}")
    if data:
        st.dataframe(pd.DataFrame(data), use_container_width=True)

elif menu == "Trading Signals":
    st.subheader("🔥 Trading Signals (inkl. Memecoins)")
    st.caption("Simulierte Signale – nur zu Bildungszwecken")
    
    cols = st.columns(3)
    i = 0
    for coin in coins:
        with cols[i % 3]:
            price = prices.get(coin.lower().replace("wif","dogwifhat").replace("shib","shiba-inu").replace("pepe","pepe").replace("bonk","bonk"), {}).get("usd", 1000)
            signal = random.choice(["STRONG BUY", "BUY", "HOLD", "SELL", "STRONG SELL
