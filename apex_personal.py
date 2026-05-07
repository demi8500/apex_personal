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
st.subheader("Trading Signals + Portfolio")

# Live Preise
@st.cache_data(ttl=30)
def get_prices():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd")
        return r.json()
    except:
        return {}

prices = get_prices()

# Portfolio
if "my_holdings" not in st.session_state:
    st.session_state.my_holdings = {"BTC": 0.0, "ETH": 0.0, "SOL": 0.0}

menu = st.sidebar.selectbox("Menü", ["Dashboard", "Trading Signals", "Holdings bearbeiten", "Neue Investition", "Live Preise"])

if menu == "Dashboard":
    total = 0.0
    data = []
    for coin, amount in st.session_state.my_holdings.items():
        if amount > 0:
            price = prices.get(coin.lower(), {}).get("usd", 0)
            value = amount * price
            total += value
            data.append({"Coin": coin, "Menge": amount, "Wert ($)": round(value, 2)})
    st.metric("Gesamtwert", f"${total:,.2f}")
    if data:
        st.dataframe(pd.DataFrame(data), use_container_width=True)

elif menu == "Trading Signals":
    st.subheader("🔥 Trading Signals")
    for coin in ["BTC", "ETH", "SOL"]:
        price = prices.get(coin.lower(), {}).get("usd", 1000)
        signal = random.choice(["STRONG BUY", "BUY", "HOLD", "SELL", "STRONG SELL"])
        if "BUY" in signal:
            st.success(f"{coin} → {signal} → ${price:,.2f}")
        elif "SELL" in signal:
            st.error(f"{coin} → {signal} → ${price:,.2f}")
        else:
            st.warning(f"{coin} → {signal} → ${price:,.2f}")

elif menu == "Holdings bearbeiten":
    st.subheader("Holdings bearbeiten")
    for coin in st.session_state.my_holdings.keys():
        st.session_state.my_holdings[coin] = st.number_input(f"{coin} Menge", value=st.session_state.my_holdings[coin], step=0.0001)
    if st.button("Speichern"):
        st.success("Gespeichert!")

elif menu == "Neue Investition":
    amount = st.number_input("Betrag USDC", min_value=10.0, value=500.0)
    coin = st.selectbox("Coin", ["BTC", "ETH", "SOL"])
    if st.button("Speichern"):
        current_price = prices.get(coin.lower(), {}).get("usd", 1000)
        st.session_state.my_holdings[coin] += amount / current_price
        st.success(f"{amount}$ in {coin} hinzugefügt!")

elif menu == "Live Preise":
    st.subheader("Live Preise")
    for coin, data in prices.items():
        st.metric(coin.upper(), f"${data['usd']:,.2f}")

st.caption("APEX Personal | Nur für dich")
