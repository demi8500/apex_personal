import streamlit as st
import pandas as pd
import requests

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

st.title("🌟 APEX Personal v6.2")
st.subheader("Viele Coins – Echte Portfolio Version")

# Viele Coins von CoinMarketCap (über CoinGecko API)
@st.cache_data(ttl=30)
def get_prices():
    try:
        ids = "bitcoin,ethereum,solana,binancecoin,ripple,dogecoin,cardano,avalanche-2,chainlink,toncoin,shiba-inu,polkadot,near-protocol,uniswap,tron,litecoin,bitcoin-cash"
        r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd")
        return r.json()
    except:
        return {}

prices = get_prices()

# Dein Portfolio
if "my_holdings" not in st.session_state:
    st.session_state.my_holdings = {
        "BTC": 0.0, "ETH": 0.0, "SOL": 0.0, "BNB": 0.0, "XRP": 0.0,
        "DOGE": 0.0, "ADA": 0.0, "AVAX": 0.0, "LINK": 0.0, "TON": 0.0,
        "SHIB": 0.0, "DOT": 0.0, "NEAR": 0.0, "UNI": 0.0, "TRX": 0.0
    }
    st.session_state.total_invested = 0.0

menu = st.sidebar.selectbox("Menü", ["Dashboard", "Holdings bearbeiten", "Neue Investition", "Live Preise", "Trading Signals", "Ziel Simulator"])

if menu == "Dashboard":
    total_value = 0.0
    data = []
    for coin, amount in st.session_state.my_holdings.items():
        if amount > 0:
            price = prices.get(coin.lower().replace("xrp", "ripple").replace("doge", "dogecoin").replace("shib", "shiba-inu").replace("dot", "polkadot").replace("near", "near-protocol").replace("uni", "uniswap").replace("trx", "tron"), {}).get("usd", 0)
            value = amount * price
            total_value += value
            data.append({"Coin": coin, "Menge": amount, "Preis": f"${price:,.4f}", "Wert ($)": round(value, 2)})
    
    st.metric("Gesamtwert Portfolio", f"${total_value:,.2f}")
    if data:
        st.dataframe(pd.DataFrame(data), use_container_width=True)
    else:
        st.info("Trage deine Holdings ein unter 'Holdings bearbeiten'")

elif menu == "Holdings bearbeiten":
    st.subheader("Deine echten Holdings")
    for coin in st.session_state.my_holdings.keys():
        st.session_state.my_hold
