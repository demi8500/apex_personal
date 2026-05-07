import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="APEX Personal", layout="wide", page_icon="🌟")

# Schönes Dark Design
st.markdown("""
<style>
    .big-title { font-size: 58px !important; font-weight: bold; }
    .stMetric { background-color: #1E1E1E; padding: 15px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("🌟 APEX Personal Portfolio Manager")
st.markdown("**Dein ultimativer privater Crypto Investment Manager**")

# ==================== SESSION STATE ====================
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {
        "total_invested": 18500.0,
        "current_value": 24780.0,
        "theme": "Balanced",
        "nft_level": "Diamond",
        "last_rebalance": "2026-04-07",
        "holdings": {
            "BTC": {"amount": 0.18, "value": 12285},
            "ETH": {"amount": 4.2, "value": 11130},
            "SOL": {"amount": 68, "value": 10064},
            "USDC": {"amount": 1301, "value": 1301}
        }
    }

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/star.png", width=70)
    st.title("APEX")
    menu = st.selectbox("Menü", [
        "Dashboard", 
        "Neue Investition", 
        "Portfolio Themes", 
        "Rebalancing & Yield", 
        "Performance Charts", 
        "Live Preise",
        "Strategie Tipps",
        "Ziel Simulator"
    ])

# ==================== DASHBOARD ====================
if menu == "Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Investiert", f"${st.session_state.portfolio['total_invested']:,.2f}")
    pnl = st.session_state.portfolio['current_value'] - st.session_state.portfolio['total_invested']
    col2.metric("Aktueller Wert", f"${st.session_state.portfolio['current_value']:,.2f}", f"↑ {((pnl / st.session_state.portfolio['total_invested']) * 100):.1f}%")
    col3.metric("NFT Level", st.session_state.portfolio["nft_level"], "🔥 Diamond")
    col4.metric("Aktives Theme", st.session_state.portfolio["theme"])

    st.subheader("📊 Deine Holdings")
    df = pd.DataFrame.from_dict(st.session_state.portfolio["holdings"], orient="index")
    st.dataframe(df, use_container_width=True)

# ==================== NEUE INVESTITION ====================
elif menu == "Neue Investition":
    st.subheader("💰 Neue Investition")
    amount = st.number_input("Betrag in USDC", min_value=100.0, value=1000.0, step=50.0)
    theme = st.selectbox("Strategie", ["Balanced", "High Yield", "AI & Tech", "Bluechip Safe", "Aggressive Growth", "Memecoin Alpha"])
    
    if st.button("JETZT INVESTIEREN", type="primary", use_container_width=True):
        st.session_state.portfolio["total_invested"] += amount
        growth = random.uniform(1.01, 1.15)
        st.session_state.portfolio["current_value"] += amount * growth
        st.session_state.portfolio["theme"] = theme
        st.success(f"✅ ${amount:,.2f} investiert in **{theme}**!")
        st.balloons()

# ==================== REBALANCING ====================
elif menu == "Rebalancing & Yield":
    st.subheader("🔄 Rebalancing & Yield")
    if st.button("Monatliches Rebalancing + Yield starten", type="primary"):
        profit = random.uniform(5.0, 25.0)
        st.session_state.portfolio["current_value"] *= (1 + profit/100)
        st.success(f"🎉 Rebalancing & Yield abgeschlossen! Gewinn diesen Monat: **+{profit:.2f}%**")
        st.snow()

# ==================== LIVE PREISE ====================
elif menu == "Live Preise":
    st.subheader("📈 Aktuelle Crypto Preise (simuliert)")
    prices = {
        "Bitcoin (BTC)": 68250,
        "Ethereum (ETH)": 2650,
        "Solana (SOL)": 148,
        "Avalanche (AVAX)": 28.5,
        "Chainlink (LINK)": 13.8
    }
    for coin, price in prices.items():
        st.metric(coin, f"${price:,}")

# ==================== CHARTS ====================
elif menu == "Performance Charts":
    st.subheader("📈 Portfolio Entwicklung")
    dates = pd.date_range(end=datetime.today(), periods=18, freq='M')
    values = [st.session_state.portfolio["total_invested"] * (1 + i*0.11) for i in range(18)]
    df = pd.DataFrame({"Datum": dates, "Wert ($)": values})
    
    fig = px.area(df, x="Datum", y="Wert ($)", title="Deine langfristige Portfolio-Entwicklung")
    st.plotly_chart(fig, use_container_width=True)

# ==================== STRATEGIE TIPPS ====================
elif menu == "Strategie Tipps":
    st.subheader("🚀 So vervielfachst du dein Investment")
    st.markdown("""
    ### Top Strategien 2026:
    - **DCA** — Jeden Monat fix einzahlen (beste Methode)
    - **Rebalancing** — Alle 4–6 Wochen durchführen
    - **Yield optimieren** — Staking & Lending nutzen
    - **Theme Rotation** — Anpassen an Marktphase
    - **Risiko streuen** — Max. 10-15% in einen Coin
    - **Langfristig denken** — 3–7 Jahre Minimum
    """)

# ==================== ZIEL SIMULATOR ====================
elif menu == "Ziel Simulator":
    st.subheader("🎯 Ziel Simulator")
    ziel = st.number_input("Dein Zielbetrag ($)", value=100000)
    monatlich = st.number_input("Monatliche Einzahlung ($)", value=500)
    
    months = 0
    current = st.session_state.portfolio["current_value"]
    while current < ziel and months < 600:
        current += monatlich
        current *= 1.0085  # ca. 10.7% jährlich
        months += 1
    
    years = months // 12
    st.success(f"Du erreichst **${ziel:,.0f}** in ca. **{years} Jahren** bei {monatlich}$ monatlich.")

st.caption("APEX Personal v3.0 — Optimale Version | Nur für dich")
