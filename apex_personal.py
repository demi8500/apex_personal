import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random

st.set_page_config(page_title="APEX Personal", layout="wide", page_icon="🌟")
st.title("🌟 APEX Personal Portfolio Manager")
st.subheader("Dein privater intelligenter Crypto Investment Manager")

# Session State
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {
        "total_invested": 12500.0,
        "current_value": 14890.0,
        "theme": "Balanced",
        "nft_level": "Gold",
        "holdings": {
            "BTC": {"amount": 0.12, "value": 8200},
            "ETH": {"amount": 2.8, "value": 7420},
            "SOL": {"amount": 45, "value": 6660},
            "USDC": {"amount": 2610, "value": 2610}
        }
    }

menu = st.sidebar.selectbox("Menü", [
    "Dashboard", "Neue Investition", "Portfolio Themes", 
    "Rebalancing & Yield", "Performance Charts", 
    "Wallet Tracking", "Strategie Tipps (Vervielfachen)"
])

if menu == "Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Investiert", f"${st.session_state.portfolio['total_invested']:,.2f}")
    pnl = st.session_state.portfolio['current_value'] - st.session_state.portfolio['total_invested']
    col2.metric("Aktueller Wert", f"${st.session_state.portfolio['current_value']:,.2f}", f"{(pnl / st.session_state.portfolio['total_invested'] * 100):+.1f}%")
    col3.metric("NFT Level", st.session_state.portfolio["nft_level"])
    col4.metric("Theme", st.session_state.portfolio["theme"])

    st.subheader("Deine Holdings")
    df = pd.DataFrame.from_dict(st.session_state.portfolio["holdings"], orient="index")
    st.dataframe(df, use_container_width=True)

elif menu == "Neue Investition":
    amount = st.number_input("Investitionsbetrag (USDC)", min_value=100.0, value=1000.0, step=100.0)
    theme = st.selectbox("Strategie", ["Balanced", "High Yield", "AI & Tech", "Bluechip Safe", "Aggressive Growth"])
    if st.button("Jetzt investieren", type="primary"):
        st.session_state.portfolio["total_invested"] += amount
        st.session_state.portfolio["current_value"] += amount * random.uniform(1.0, 1.08)
        st.session_state.portfolio["theme"] = theme
        st.success(f"${amount:,.2f} erfolgreich investiert!")
        st.balloons()

elif menu == "Rebalancing & Yield":
    if st.button("Monatliches Rebalancing + Yield ausführen", type="primary"):
        profit = random.uniform(3.0, 18.0)
        st.session_state.portfolio["current_value"] *= (1 + profit/100)
        st.success(f"✅ Rebalancing fertig! Monatsgewinn: **+{profit:.2f}%**")

elif menu == "Performance Charts":
    dates = pd.date_range(end=datetime.today(), periods=12, freq='M')
    values = [st.session_state.portfolio["total_invested"] * (1 + i*0.085) for i in range(12)]
    df = pd.DataFrame({"Monat": dates, "Wert ($)": values})
    fig = px.line(df, x="Monat", y="Wert ($)", title="Portfolio Entwicklung")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Strategie Tipps (Vervielfachen)":
    st.markdown("""
    ### 🔥 So vervielfachst du dein Investment:
    - DCA (jeden Monat fix einzahlen)
    - Regelmäßiges Rebalancing
    - Yield maximieren (Staking)
    - Theme Rotation (Bull / Bear)
    - Nie alles in einen Coin
    - Langfristig denken (3–5 Jahre)
    """)

st.caption("APEX Personal Online Version | Nur für dich | 2026")
