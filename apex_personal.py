import streamlit as st
import random

st.set_page_config(page_title="APEX Personal", layout="wide")

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 APEX Personal")
    pw = st.text_input("Passwort", type="password")
    if st.button("Login"):
        if pw == "bnc2500":
            st.session_state.auth = True
            st.rerun()
    st.stop()

st.title("🌟 APEX Personal")
st.subheader("Trading Signals")

coins = ["BTC", "ETH", "SOL", "DOGE", "SHIB", "PEPE", "BONK", "WIF"]

st.write("### 🔥 Trading Signals")
for coin in coins:
    signal = random.choice(["STRONG BUY", "BUY", "HOLD", "SELL", "STRONG SELL"])
    if "BUY" in signal:
        st.success(f"**{coin}** → {signal}")
    elif "SELL" in signal:
        st.error(f"**{coin}** → {signal}")
    else:
        st.warning(f"**{coin}** → {signal}")

st.caption("Einfache Version - Nur für dich")
