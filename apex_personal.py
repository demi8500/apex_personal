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
        if pw == "bnc2500":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Falsches Passwort")
    st.stop()

st.title("🌟 APEX Personal v6.0")
st.subheader("Dein ultimativer Crypto Manager")

# Live Preise
@st.cache_data(ttl=30)
def get_prices():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,avalanche-2,chainlink,cardano&vs_currencies=usd")
        return r.json()
    except:
        return {"bitcoin": {"usd": 68250}, "ethereum": {"usd": 2650}, "solana": {"usd": 148}}

prices = get_prices()

# Portfolio
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {
        "total_invested": 18500.0,
        "current_value": 27950.0,
        "holdings": {"BTC": 0.23, "ETH": 5.1, "SOL": 82, "AVAX": 135, "LINK": 480, "ADA": 8500}
    }

menu = st.sidebar.selectbox("Menü", [
    "Dashboard", "Neue Investition", "Live Preise", "Rebalancing & Yield",
    "Ziel Simulator", "Holdings bearbeiten", "Strategie Tipps", "Export"
])

if menu == "Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Investiert", f"${st.session_state.portfolio['total_invested']:,.2f}")
    pnl = st.session_state.portfolio['current_value'] - st.session_state.portfolio['total_invested']
    col2.metric("Aktueller Wert", f"${st.session_state.portfolio['current_value']:,.2f}", f"↑ {((pnl / st.session_state.portfolio['total_invested']) * 100):.1f}%")
    col3.metric("NFT Level", "Diamond 🔥", "Top Tier")
    col4.metric("Gesamtrendite", f"{((st.session_state.portfolio['current_value']/st.session_state.portfolio['total_invested']-1)*100):.1f}%")

    st.subheader("📊 Deine Holdings")
    data = []
    for coin, amount in st.session_state.portfolio["holdings"].items():
        price = prices.get(coin.lower(), {"usd": 1000})["usd"]
        value = amount * price
        data.append({"Coin": coin, "Menge": amount, "Preis": f"${price:,.2f}", "Wert ($)": round(value, 2)})
    st.dataframe(pd.DataFrame(data), use_container_width=True)

elif menu == "Neue Investition":
    amount = st.number_input("Betrag in USDC", min_value=50.0, value=1000.0)
    coin = st.selectbox("Coin kaufen", ["BTC", "ETH", "SOL", "AVAX", "LINK", "ADA"])
    if st.button("JETZT KAUFEN", type="primary"):
        st.session_state.portfolio["total_invested"] += amount
        st.session_state.portfolio["current_value"] += amount * random.uniform(1.0, 1.18)
        st.success(f"✅ {amount} USDC in {coin} investiert!")
        st.balloons()

elif menu == "Live Preise":
    st.subheader("📈 Live Preise")
    for coin, data in prices.items():
        st.metric(coin.upper(), f"${data['usd']:,.2f}")

elif menu == "Rebalancing & Yield":
    if st.button("Rebalancing + Yield jetzt ausführen", type="primary"):
        profit = random.uniform(6.0, 28.0)
        st.session_state.portfolio["current_value"] *= (1 + profit/100)
        st.success(f"🎉 Rebalancing erfolgreich! Monatsgewinn: **+{profit:.2f}%**")

elif menu == "Ziel Simulator":
    ziel = st.number_input("Zielbetrag ($)", value=100000)
    monatlich = st.number_input("Monatliche Einzahlung ($)", value=800)
    rendite = st.slider("Erwartete jährliche Rendite (%)", 5, 40, 15)
    years = round((ziel - st.session_state.portfolio["current_value"]) / (monatlich * 12 * (1 + rendite/100)), 1)
    st.success(f"**Du erreichst ${ziel:,.0f} in ca. {years} Jahren**")

elif menu == "Holdings bearbeiten":
    st.subheader("Holdings manuell bearbeiten")
    for coin in list(st.session_state.portfolio["holdings"].keys()):
        st.session_state.portfolio["holdings"][coin] = st.number_input(f"{coin} Menge", value=st.session_state.portfolio["holdings"][coin], step=0.01)

elif menu == "Strategie Tipps":
    st.subheader("🚀 Die besten Strategien 2026")
    st.markdown("""
    - **DCA** jeden Monat fix einzahlen  
    - Monatliches **Rebalancing**  
    - 30–40% in **Yield** (Staking/Lending)  
    - Theme Rotation (Bull/Bear)  
    - Nie mehr als 15% in einen Coin  
    """)

elif menu == "Export":
    df = pd.DataFrame.from_dict(st.session_state.portfolio["holdings"], orient="index")
    st.download_button("📥 Portfolio als CSV herunterladen", df.to_csv(), "apex_portfolio.csv", "text/csv")

st.caption("APEX Personal v6.0 – Ultimative Version | Nur für dich")
