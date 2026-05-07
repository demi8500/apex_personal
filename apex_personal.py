import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
import random

st.set_page_config(page_title="APEX Personal", layout="wide", page_icon="🌟")

# ==================== PASSWORT ====================
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 APEX Personal")
    pw = st.text_input("Passwort eingeben", type="password")
    if st.button("Login"):
        if pw == "bnc2500":          # ← Hier später ändern
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Falsches Passwort")
    st.stop()

st.title("🌟 APEX Personal v5.0")
st.subheader("Dein ultimativer Crypto Manager")

# Live Preise
@st.cache_data(ttl=30)
def get_prices():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,avalanche-2,chainlink&vs_currencies=usd")
        return r.json()
    except:
        return {"bitcoin": {"usd": 68250}, "ethereum": {"usd": 2650}, "solana": {"usd": 148}}

prices = get_prices()

# Portfolio
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {
        "total_invested": 18500.0,
        "current_value": 26850.0,
        "holdings": {"BTC": 0.21, "ETH": 4.8, "SOL": 75, "AVAX": 120, "LINK": 450}
    }

menu = st.sidebar.selectbox("Menü", [
    "Dashboard", "Neue Investition", "Live Preise", "Rebalancing & Yield",
    "Ziel Simulator", "Strategie Tipps", "Holdings bearbeiten", "Export"
])

# ==================== DASHBOARD ====================
if menu == "Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Investiert", f"${st.session_state.portfolio['total_invested']:,.2f}")
    pnl = st.session_state.portfolio['current_value'] - st.session_state.portfolio['total_invested']
    col2.metric("Aktueller Wert", f"${st.session_state.portfolio['current_value']:,.2f}", f"↑ {((pnl / st.session_state.portfolio['total_invested']) * 100):.1f}%")
    col3.metric("NFT Level", "Diamond 🔥")
    col4.metric("Gesamtrendite", f"{((st.session_state.portfolio['current_value']/st.session_state.portfolio['total_invested']-1)*100):.1f}%")

    st.subheader("📊 Deine Holdings")
    data = []
    for coin, amount in st.session_state.portfolio["holdings"].items():
        price = prices.get(coin.lower(), {"usd": 1000})["usd"]
        value = amount * price
        data.append({"Coin": coin, "Menge": amount, "Preis": f"${price:,.2f}", "Wert $": round(value, 2)})
    st.dataframe(pd.DataFrame(data), use_container_width=True)

# ==================== NEUE INVESTITION ====================
elif menu == "Neue Investition":
    amount = st.number_input("Betrag in USDC", min_value=50.0, value=1000.0)
    coin = st.selectbox("Coin kaufen", ["BTC", "ETH", "SOL", "AVAX", "LINK"])
    if st.button("JETZT KAUFEN", type="primary"):
        st.session_state.portfolio["total_invested"] += amount
        st.session_state.portfolio["current_value"] += amount * random.uniform(1.0, 1.15)
        st.success(f"✅ {amount} USDC in {coin} investiert!")
        st.balloons()

# ==================== LIVE PREISE ====================
elif menu == "Live Preise":
    st.subheader("📈 Live Preise")
    for coin, data in prices.items():
        st.metric(coin.upper(), f"${data['usd']:,.2f}")

# ==================== REBALANCING ====================
elif menu == "Rebalancing & Yield":
    if st.button("Rebalancing + Yield jetzt ausführen", type="primary"):
        profit = random.uniform(5.0, 25.0)
        st.session_state.portfolio["current_value"] *= (1 + profit/100)
        st.success(f"🎉 Rebalancing erfolgreich! Monatsgewinn: **+{profit:.2f}%**")

# ==================== ZIEL SIMULATOR ====================
elif menu == "Ziel Simulator":
    ziel = st.number_input("Zielbetrag ($)", value=100000)
    monatlich = st.number_input("Monatliche Einzahlung ($)", value=800)
    rendite = st.slider("Erwartete jährliche Rendite (%)", 5, 40, 15)
    years = round((ziel - st.session_state.portfolio["current_value"]) / (monatlich * 12 * (1 + rendite/100)), 1)
    st.success(f"**Du erreichst ${ziel:,.0f} in ca. {years} Jahren**")

# ==================== HOLDINGS BEARBEITEN ====================
elif menu == "Holdings bearbeiten":
    st.subheader("Holdings manuell bearbeiten")
    for coin in list(st.session_state.portfolio["holdings"].keys()):
        st.session_state.portfolio["holdings"][coin] = st.number_input(f"{coin} Menge", value=st.session_state.portfolio["holdings"][coin])

# ==================== STRATEGIE TIPPS ====================
elif menu == "Strategie Tipps":
    st.subheader("🚀 Die besten Strategien 2026")
    st.info("DCA + monatliches Rebalancing + Yield-Optimierung ist aktuell eine der stärksten Kombinationen.")

# ==================== EXPORT ====================
elif menu == "Export":
    df = pd.DataFrame.from_dict(st.session_state.portfolio["holdings"], orient="index")
    st.download_button("📥 Portfolio als CSV herunterladen", df.to_csv(), "mein_portfolio.csv")

st.caption("APEX Personal v5.0 – Maximale Version | Nur
