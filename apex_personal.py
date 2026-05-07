import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
import random

st.set_page_config(page_title="APEX Personal", layout="wide", page_icon="🌟")

st.title("🌟 APEX Personal – Dein Crypto Manager")
st.subheader("Voll funktionsfähige Demo-Version")

# Passwort (kannst du später ändern)
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    pw = st.text_input("Passwort eingeben", type="password")
    if st.button("Login"):
        if pw == "bnc2500":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Falsches Passwort")
    st.stop()

# Live Preise
@st.cache_data(ttl=30)
def get_prices():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd")
        return r.json()
    except:
        return {"bitcoin": {"usd": 68250}, "ethereum": {"usd": 2650}, "solana": {"usd": 148}}

prices = get_prices()

# Portfolio
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {
        "total_invested": 18500,
        "current_value": 25980,
        "holdings": {"BTC": 0.21, "ETH": 4.8, "SOL": 75}
    }

menu = st.sidebar.selectbox("Menü", ["Dashboard", "Neue Investition", "Live Preise", "Rebalancing", "Ziel Simulator", "Strategie"])

if menu == "Dashboard":
    st.metric("Aktueller Portfolio Wert", f"${st.session_state.portfolio['current_value']:,.2f}", f"+{((st.session_state.portfolio['current_value']/st.session_state.portfolio['total_invested']-1)*100):.1f}%")
    st.dataframe(pd.DataFrame.from_dict(st.session_state.portfolio["holdings"], orient="index"), use_container_width=True)

elif menu == "Neue Investition":
    amount = st.number_input("Betrag USDC", 100, 5000, 1000)
    coin = st.selectbox("Coin", ["BTC", "ETH", "SOL"])
    if st.button("Kaufen"):
        st.session_state.portfolio["current_value"] += amount
        st.success(f"{amount}$ {coin} gekauft!")

elif menu == "Live Preise":
    for coin, data in prices.items():
        st.metric(coin.upper(), f"${data['usd']:,.2f}")

elif menu == "Rebalancing":
    if st.button("Rebalancing jetzt ausführen"):
        st.success("Rebalancing erfolgreich! +8.4% Gewinn simuliert")

elif menu == "Ziel Simulator":
    ziel = st.number_input("Ziel ($)", 50000, 1000000, 100000)
    monat = st.number_input("Monatlich einzahlen", 200, 5000, 800)
    st.success(f"Bei 12% jährlich erreichst du dein Ziel in ca. **{round((ziel / (monat*12*1.12)),1)} Jahren**")

elif menu == "Strategie":
    st.write("**Empfohlene Strategie:** DCA + monatliches Rebalancing + 30% in Yield")

st.caption("APEX Personal – Starke Version | Nur für dich")
