import streamlit as st
import pandas as pd
import requests
import random
from datetime import datetime

st.set_page_config(page_title="APEX Personal", layout="wide", page_icon="🌟")

# Passwort
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 APEX Personal")
    pw = st.text_input("Passwort", type="password")
    if st.button("Login"):
        if pw == "bnc2500":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Falsches Passwort")
    st.stop()

st.title("🌟 APEX Personal – Echte Version")
st.subheader("Deine echten Coins tracken & managen")

# Live Preise
@st.cache_data(ttl=30)
def get_prices():
    try:
        ids = "bitcoin,ethereum,solana,avalanche-2,chainlink,cardano"
        r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd")
        return r.json()
    except:
        return {}

prices = get_prices()

# Dein Portfolio
if "my_holdings" not in st.session_state:
    st.session_state.my_holdings = {"BTC": 0.0, "ETH": 0.0, "SOL": 0.0, "AVAX": 0.0, "LINK": 0.0, "ADA": 0.0}
    st.session_state.total_invested = 0.0

menu = st.sidebar.selectbox("Menü", ["Dashboard", "Holdings bearbeiten", "Neue Investition", "Live Preise", "Ziel Simulator", "Export"])

if menu == "Dashboard":
    total_value = 0.0
    data = []
    for coin, amount in st.session_state.my_holdings.items():
        if amount > 0:
            price = prices.get(coin.lower(), {}).get("usd", 0)
            value = amount * price
            total_value += value
            data.append({"Coin": coin, "Menge": amount, "Preis": f"${price:,.2f}", "Wert ($)": round(value, 2)})

    st.metric("Gesamtwert", f"${total_value:,.2f}")
    if data:
        st.dataframe(pd.DataFrame(data), use_container_width=True)
    else:
        st.info("Noch keine Coins eingetragen → 'Holdings bearbeiten'")

elif menu == "Holdings bearbeiten":
    st.subheader("Deine echten Holdings eintragen")
    for coin in st.session_state.my_holdings.keys():
        st.session_state.my_holdings[coin] = st.number_input(f"{coin} Menge", value=st.session_state.my_holdings[coin], step=0.0001, format="%.4f")
    if st.button("Speichern"):
        st.success("Holdings gespeichert!")

elif menu == "Neue Investition":
    amount = st.number_input("Betrag (USDC)", min_value=10.0, value=500.0)
    coin = st.selectbox("Coin", ["BTC", "ETH", "SOL", "AVAX", "LINK", "ADA"])
    if st.button("Investition speichern"):
        st.session_state.total_invested += amount
        st.session_state.my_holdings[coin] += amount / prices.get(coin.lower(), {}).get("usd", 1000)
        st.success(f"{amount}$ in {coin} investiert!")

elif menu == "Live Preise":
    st.subheader("Live Preise")
    for coin, data in prices.items():
        st.metric(coin.upper(), f"${data.get('usd', 0):,.2f}")

elif menu == "Ziel Simulator":
    ziel = st.number_input("Ziel ($)", value=100000)
    monatlich = st.number_input("Monatlich einzahlen", value=800)
    st.success(f"Bei ~12% jährlich ca. {round((ziel / (monatlich*12*1.1)),1)} Jahre")

elif menu == "Export":
    df = pd.DataFrame.from_dict(st.session_state.my_holdings, orient="index", columns=["Menge"])
    st.download_button("Portfolio als CSV herunterladen", df.to_csv(), "mein_portfolio.csv")

st.caption("APEX Personal – Echte Version | Nur für dich")
