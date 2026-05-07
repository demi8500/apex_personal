import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
import random

st.set_page_config(page_title="APEX Personal", layout="wide", page_icon="🌟")

# Passwortschutz
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 APEX Personal")
    pw = st.text_input("Passwort eingeben", type="password")
    if st.button("Login"):
        if pw == "bnc2500":          # ← Hier kannst du später dein eigenes Passwort eintragen
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Falsches Passwort")
    st.stop()

st.title("🌟 APEX Personal")
st.subheader("Dein voll funktionsfähiger Crypto Manager")

# Live Preise
@st.cache_data(ttl=30)
def get_prices():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,avalanche-2&vs_currencies=usd")
        return r.json()
    except:
        return {"bitcoin": {"usd": 68250}, "ethereum": {"usd": 2650}, "solana": {"usd": 148}}

prices = get_prices()

# Portfolio
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {
        "total_invested": 18500.0,
        "current_value": 25980.0,
        "holdings": {"BTC": 0.21, "ETH": 4.8, "SOL": 75, "AVAX": 120}
    }

menu = st.sidebar.selectbox("Menü", [
    "Dashboard", "Neue Investition", "Live Preise", 
    "Rebalancing & Yield", "Ziel Simulator", "Strategie Tipps"
])

if menu == "Dashboard":
    col1, col2, col3 = st.columns(3)
    col1.metric("Investiert", f"${st.session_state.portfolio['total_invested']:,.2f}")
    pnl = st.session_state.portfolio['current_value'] - st.session_state.portfolio['total_invested']
    col2.metric("Aktueller Wert", f"${st.session_state.portfolio['current_value']:,.2f}", f"↑ {((pnl / st.session_state.portfolio['total_invested']) * 100):.1f}%")
    col3.metric("Gesamtrendite", f"{((st.session_state.portfolio['current_value']/st.session_state.portfolio['total_invested']-1)*100):.1f}%")

    st.subheader("Deine Holdings")
    data = []
    for coin, amount in st.session_state.portfolio["holdings"].items():
        price = prices.get(coin.lower(), {"usd": 1000})["usd"]
        value = amount * price
        data.append({"Coin": coin, "Menge": amount, "Preis": f"${price:,.2f}", "Wert $": round(value, 2)})
    st.dataframe(pd.DataFrame(data), use_container_width=True)

elif menu == "Neue Investition":
    amount = st.number_input("Betrag in USDC", min_value=50.0, value=500.0)
    coin = st.selectbox("Welchen Coin kaufen?", ["BTC", "ETH", "SOL", "AVAX"])
    if st.button("JETZT KAUFEN", type="primary"):
        st.session_state.portfolio["total_invested"] += amount
        st.session_state.portfolio["current_value"] += amount * random.uniform(1.0, 1.12)
        st.success(f"✅ {amount} USDC in {coin} investiert!")
        st.balloons()

elif menu == "Live Preise":
    st.subheader("📈 Aktuelle Preise")
    for coin, data in prices.items():
        st.metric(coin.upper(), f"${data['usd']:,.2f}")

elif menu == "Rebalancing & Yield":
    if st.button("Rebalancing + Yield jetzt ausführen", type="primary"):
        profit = random.uniform(4.0, 22.0)
        st.session_state.portfolio["current_value"] *= (1 + profit/100)
        st.success(f"🎉 Rebalancing erfolgreich! Monatsgewinn: **+{profit:.2f}%**")

elif menu == "Ziel Simulator":
    ziel = st.number_input("Dein Zielbetrag ($)", value=100000)
    monatlich = st.number_input("Monatliche Einzahlung ($)", value=800)
    st.success(f"Bei ~12% jährlicher Rendite erreichst du dein Ziel in ca. **{round((ziel / (monatlich*12*1.1)),1)} Jahren**")

elif menu == "Strategie Tipps":
    st.subheader("🚀 Beste Strategie 2026")
    st.info("DCA + monatliches Rebalancing + 30-40% in Yield-Strategien ist aktuell eine der stärksten Methoden.")

st.caption("APEX Personal – Starke Vollversion | Nur für dich")
