import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="APEX Personal", layout="wide", page_icon="🌟")

# Passwortschutz
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

st.title("🌟 APEX Personal – Echte Portfolio Version")
st.subheader("Deine echten Investments tracken")

# Live Preise
@st.cache_data(ttl=30)
def get_prices():
    try:
        coins = "bitcoin,ethereum,solana,avalanche-2,chainlink,cardano,binancecoin"
        r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coins}&vs_currencies=usd")
        return r.json()
    except:
        return {}

prices = get_prices()

# Portfolio (wird gespeichert)
if "my_holdings" not in st.session_state:
    st.session_state.my_holdings = {
        "BTC": 0.0, "ETH": 0.0, "SOL": 0.0, "AVAX": 0.0, 
        "LINK": 0.0, "ADA": 0.0, "BNB": 0.0
    }
    st.session_state.total_invested = 0.0

menu = st.sidebar.selectbox("Menü", ["Dashboard", "Holdings bearbeiten", "Neue Investition", "Live Preise", "Ziel Simulator"])

# ==================== DASHBOARD ====================
if menu == "Dashboard":
    total_value = 0.0
    data = []
    for coin, amount in st.session_state.my_holdings.items():
        price = prices.get(coin.lower(), {}).get("usd", 0)
        value = amount * price
        total_value += value
        if amount > 0:
            data.append({
                "Coin": coin,
                "Menge": amount,
                "Aktueller Preis": f"${price:,.2f}",
                "Wert ($)": round(value, 2)
            })

    col1, col2 = st.columns(2)
    col1.metric("Gesamtwert Portfolio", f"${total_value:,.2f}")
    col2.metric("Investiert (manuell)", f"${st.session_state.total_invested:,.2f}")

    if data:
        st.dataframe(pd.DataFrame(data), use_container_width=True)
    else:
        st.info("Noch keine Holdings eingetragen. Gehe zu 'Holdings bearbeiten'.")

# ==================== HOLDINGS BEARBEITEN ====================
elif menu == "Holdings bearbeiten":
    st.subheader("Deine echten Holdings eintragen / bearbeiten")
    new_holdings = {}
    for coin in st.session_state.my_holdings.keys():
        new_holdings[coin] = st.number_input(f"{coin} Menge", value=st.session_state.my_holdings[coin], step=0.0001, format="%.4f")
    
    if st.button("Speichern"):
        st.session_state.my_holdings = new_holdings
        st.success("Holdings gespeichert!")

# ==================== NEUE INVESTITION ====================
elif menu == "Neue Investition":
    amount = st.number_input("Investierter Betrag (USDC)", min_value=10.0, value=500.0)
    coin = st.selectbox("In welchen Coin?", ["BTC", "ETH", "SOL", "AVAX", "LINK", "ADA", "BNB"])
    if st.button("Investition speichern"):
        st.session_state.total_invested += amount
        current = st.session_state.my_holdings[coin]
        st.session_state.my_holdings[coin] = current + (amount / prices.get(coin.lower(), {}).get("usd", 1000))
        st.success(f"✅ {amount}$ in {coin} investiert und gespeichert!")

# ==================== Live Preise & Simulator ====================
elif menu == "Live Preise":
    st.subheader("📈 Aktuelle Preise")
    for coin, data in prices.items():
        st.metric(coin.upper(), f"${data['usd']:,.2f}")

elif menu == "Ziel Simulator":
    ziel = st.number_input("Zielbetrag ($)", value=100000)
    monatlich = st.number_input("Monatliche Einzahlung", value=800)
    st.info("Der Simulator wird in der nächsten Version noch genauer.")

st.caption("APEX Personal – Echte Portfolio Version | Nur für dich")
