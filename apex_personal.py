import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random

# Schönes Design
st.set_page_config(page_title="APEX Personal", layout="wide", page_icon="🌟")
st.markdown("""
    <style>
    .big-font {font-size: 52px !important; font-weight: bold;}
    .metric-value {font-size: 28px !important;}
    </style>
    """, unsafe_allow_html=True)

st.title("🌟 APEX Personal Portfolio Manager")
st.markdown("**Dein privater intelligenter Crypto Investment Manager**")

# Session State
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {
        "total_invested": 12500.0,
        "current_value": 15890.0,
        "theme": "Balanced",
        "nft_level": "Diamond",
        "holdings": {
            "BTC": {"amount": 0.135, "value": 9200},
            "ETH": {"amount": 3.1, "value": 8215},
            "SOL": {"amount": 52, "value": 7696},
            "USDC": {"amount": 2779, "value": 2779}
        }
    }

# Sidebar mit besserem Design
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/star.png", width=80)
    st.title("APEX")
    menu = st.selectbox("Menü", [
        "Dashboard", 
        "Neue Investition", 
        "Portfolio Themes", 
        "Rebalancing & Yield", 
        "Performance Charts", 
        "Strategie Tipps"
    ])

# ==================== DASHBOARD ====================
if menu == "Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("**Investiert**", f"${st.session_state.portfolio['total_invested']:,.2f}")
    pnl = st.session_state.portfolio['current_value'] - st.session_state.portfolio['total_invested']
    col2.metric("**Aktueller Wert**", f"${st.session_state.portfolio['current_value']:,.2f}", f"↑ {((pnl / st.session_state.portfolio['total_invested']) * 100):.1f}%")
    col3.metric("**NFT Level**", st.session_state.portfolio["nft_level"], "🔥")
    col4.metric("**Aktives Theme**", st.session_state.portfolio["theme"])

    st.subheader("📊 Deine Holdings")
    df = pd.DataFrame.from_dict(st.session_state.portfolio["holdings"], orient="index")
    st.dataframe(df, use_container_width=True, height=300)

# ==================== NEUE INVESTITION ====================
elif menu == "Neue Investition":
    st.subheader("💰 Neue Investition")
    amount = st.number_input("Betrag in USDC", min_value=100.0, value=1000.0, step=100.0)
    theme = st.selectbox("Strategie wählen", 
                        ["Balanced", "High Yield", "AI & Tech", "Bluechip Safe", "Aggressive Growth", "Memecoin Alpha"])
    
    if st.button("Jetzt investieren", type="primary", use_container_width=True):
        st.session_state.portfolio["total_invested"] += amount
        growth = random.uniform(1.02, 1.12)
        st.session_state.portfolio["current_value"] += amount * growth
        st.session_state.portfolio["theme"] = theme
        st.success(f"✅ ${amount:,.2f} erfolgreich investiert in **{theme}**!")
        st.balloons()

# ==================== Weitere Menüs ====================
elif menu == "Rebalancing & Yield":
    st.subheader("🔄 Monatliches Rebalancing")
    if st.button("Rebalancing + Yield jetzt ausführen", type="primary"):
        profit = random.uniform(4.0, 22.0)
        st.session_state.portfolio["current_value"] *= (1 + profit/100)
        st.success(f"🎉 Rebalancing abgeschlossen! Monatsgewinn: **+{profit:.2f}%**")
        st.snow()

elif menu == "Performance Charts":
    st.subheader("📈 Portfolio Entwicklung")
    dates = pd.date_range(end=datetime.today(), periods=12, freq='M')
    values = [st.session_state.portfolio["total_invested"] * (1 + i*0.095) for i in range(12)]
    df = pd.DataFrame({"Monat": dates, "Portfolio Wert ($)": values})
    fig = px.line(df, x="Monat", y="Portfolio Wert ($)", title="Deine Portfolio-Performance")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Strategie Tipps":
    st.subheader("🚀 So vervielfachst du dein Geld")
    st.markdown("""
    ### Die besten Strategien:
    - **DCA** — Jeden Monat automatisch einzahlen
    - **Rebalancing** — Regelmäßig Gewinner mitnehmen
    - **Yield Farming** — Passive Einnahmen durch Staking
    - **Theme Rotation** — Anpassen an Bull/Bear Markt
    - **Risikomanagement** — Nie mehr als 10-15% in einen Coin
    - **Langfristig denken** — 3–7 Jahre halten
    """)

st.caption("APEX Personal v2.0 — Schöner & Stärker | Nur für dich")
