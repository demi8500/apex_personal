# app.py - APEX Personal
# Single-file Streamlit App
# Passwort: bnc2500
# Benötigt: streamlit, requests, pandas
# Installation: pip install streamlit requests pandas

import streamlit as st
import requests
import pandas as pd
import time
import math

# --------------------------
# Konfiguration & Styling
# --------------------------
st.set_page_config(page_title="APEX Personal", layout="wide", initial_sidebar_state="expanded")

# Dark modern CSS
st.markdown(
    """
    <style>
    /* Hintergrund & Text */
    .reportview-container, .main, .block-container {
        background-color: #0b1020;
        color: #d6e1ff;
    }
    /* Sidebar */
    .css-1d391kg .css-1d391kg { background-color: #0b1020; }
    .stButton>button {
        background-color: #0f62fe;
        color: white;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #0f1724;
        color: #d6e1ff;
        border: 1px solid #223;
    }
    .stSelectbox>div>div>div {
        background-color: #0f1724;
        color: #d6e1ff;
    }
    /* Karten */
    .card {
        background: #0f1724;
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #233;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------
# Globals: Coin mapping
# --------------------------
# Map symbol to CoinGecko id
COINS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "DOGE": "dogecoin",
    "SHIB": "shiba-inu",
    "PEPE": "pepe",
    "BONK": "bonk",
    "WIF": "wif",
    "FLOKI": "floki",
    "ADA": "cardano",
    "AVAX": "avalanche-2",
    "LINK": "chainlink",
    "TON": "toncoin",
}

COIN_SYMBOLS = list(COINS.keys())
COIN_IDS = list(COINS.values())

# --------------------------
# Utility: CoinGecko price fetch
# --------------------------
def fetch_prices(symbols):
    # symbols: list of symbols like ["BTC","ETH"]
    ids = ",".join([COINS[s] for s in symbols])
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ids,
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    # Build dict: symbol -> {price, change_24h}
    out = {}
    for sym in symbols:
        cid = COINS[sym]
        entry = data.get(cid, {})
        price = entry.get("usd", None)
        change = entry.get("usd_24h_change", None)
        out[sym] = {"price": price, "change_24h": change}
    return out

# --------------------------
# Session state initial
# --------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "holdings" not in st.session_state:
    # default demo holdings (can be empty)
    st.session_state.holdings = {
        "BTC": 0.02,
        "ETH": 0.3,
        "DOGE": 1000,
        "SHIB": 2000000
    }
if "last_prices" not in st.session_state:
    st.session_state.last_prices = {}
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = 0

# --------------------------
# Authentication (simple)
# --------------------------
def login():
    st.markdown("<h3>APEX Personal — Login</h3>", unsafe_allow_html=True)
    pwd = st.text_input("Passwort", type="password")
    if st.button("Anmelden"):
        if pwd == "bnc2500":
            st.session_state.authenticated = True
            st.success("Erfolgreich angemeldet")
            st.experimental_rerun()
        else:
            st.error("Falsches Passwort")

if not st.session_state.authenticated:
    login()
    st.stop()

# --------------------------
# Sidebar Menü
# --------------------------
st.sidebar.title("APEX Personal")
menu = st.sidebar.radio("Menü", ["Dashboard", "Trading Signals", "Holdings bearbeiten", "Neue Investition", "Live Preise", "Ziel Simulator"])

# Refresh prices button
if st.sidebar.button("Preise aktualisieren"):
    st.session_state.last_refresh = 0  # force refresh

# --------------------------
# Helper: get prices with caching (10s)
# --------------------------
def get_prices_cached():
    now = time.time()
    if now - st.session_state.last_refresh > 10:
        try:
            prices = fetch_prices(COIN_SYMBOLS)
            st.session_state.last_prices = prices
            st.session_state.last_refresh = now
        except Exception as e:
            st.error(f"Fehler beim Abrufen der Preise: {e}")
            # keep old prices if exist
    return st.session_state.last_prices

# --------------------------
# Helper: portfolio calculations
# --------------------------
def portfolio_df(holdings, prices):
    rows = []
    for sym, amount in holdings.items():
        pinfo = prices.get(sym, {})
        price = pinfo.get("price", None)
        value = (price * amount) if price is not None else None
        change24 = pinfo.get("change_24h", None)
        rows.append({
            "Coin": sym,
            "Menge": amount,
            "Preis (USD)": price,
            "Wert (USD)": value,
            "24h %": change24
        })
    df = pd.DataFrame(rows)
    return df

# --------------------------
# Trading signal logic (einfach, heuristisch)
# --------------------------
def trading_signal(change24):
    # change24 in percent
    if change24 is None:
        return "HOLD"
    if change24 >= 10:
        return "STRONG BUY"
    if 2 <= change24 < 10:
        return "BUY"
    if -2 < change24 < 2:
        return "HOLD"
    if -10 < change24 <= -2:
        return "SELL"
    return "STRONG SELL"

# Colors for signals
SIGNAL_COLORS = {
    "STRONG BUY": "#007a3d",
    "BUY": "#0bad4f",
    "HOLD": "#ffc107",
    "SELL": "#ff6b6b",
    "STRONG SELL": "#c62828"
}

# --------------------------
# Pages
# --------------------------
prices = get_prices_cached()

if menu == "Dashboard":
    st.header("Dashboard")
    df = portfolio_df(st.session_state.holdings, prices)
    total_value = df["Wert (USD)"].sum()
    # approximate percent change of portfolio using weighted 24h change
    if df["Wert (USD)"].notna().any():
        # weight by current value and apply percentage
        weighted_change = 0.0
        denom = 0.0
        for _, row in df.iterrows():
            if row["Wert (USD)"] is not None and row["24h %"] is not None:
                denom += row["Wert (USD)"]
                weighted_change += row["Wert (USD)"] * (row["24h %"] / 100.0)
        pct_change = (weighted_change / denom * 100.0) if denom > 0 else 0.0
    else:
        pct_change = 0.0

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Gesamtwert")
        st.markdown(f"<h2>${total_value:,.2f}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Portfolio Veränderung (24h geschätzt)")
        color = "#d6e1ff" if pct_change == 0 else ("#4caf50" if pct_change > 0 else "#ef5350")
        st.markdown(f"<h3 style='color:{color}'>{pct_change:+.2f}%</h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### Holdings Übersicht")
    # Show table, allow sorting
    display_df = df.copy()
    display_df["Preis (USD)"] = display_df["Preis (USD)"].map(lambda x: f"${x:,.4f}" if pd.notna(x) else "N/A")
    display_df["Wert (USD)"] = display_df["Wert (USD)"].map(lambda x: f"${x:,.2f}" if pd.notna(x) else "N/A")
    display_df["24h %"] = display_df["24h %"].map(lambda x: f"{x:+.2f}%" if pd.notna(x) else "N/A")
    st.dataframe(display_df.style.format({"Menge": "{:.8f}"}), use_container_width=True)

elif menu == "Trading Signals":
    st.header("Trading Signals")
    st.markdown("Signale basieren auf 24h %-Änderung (heuristisch).")
    signals = []
    for sym in COIN_SYMBOLS:
        info = prices.get(sym, {})
        price = info.get("price", None)
        chg = info.get("change_24h", None)
        sig = trading_signal(chg)
        signals.append((sym, price, chg, sig))
    # Render cards in grid
    cols = st.columns(3)
    idx = 0
    for sym, price, chg, sig in signals:
        c = cols[idx % 3]
        with c:
            color = SIGNAL_COLORS.get(sig, "#222")
            st.markdown(f"<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='margin:0'>{sym}</h4>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:18px'>Preis: <b>${price:,.4f}</b></div>" if price is not None else "<div>Preis: N/A</div>", unsafe_allow_html=True)
            chg_text = f"{chg:+.2f}%" if chg is not None else "N/A"
            st.markdown(f"<div>24h: {chg_text}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-top:8px;padding:8px;border-radius:6px;background:{color};color:white;text-align:center'><b>{sig}</b></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        idx += 1

elif menu == "Holdings bearbeiten":
    st.header("Holdings bearbeiten")
    st.markdown("Gib die Menge für jeden Coin ein und speichere.")
    # Editable form
    with st.form("edit_holdings"):
        new_holdings = {}
        for sym in COIN_SYMBOLS:
            cur = st.session_state.holdings.get(sym, 0.0)
            val = st.number_input(f"{sym} Menge", min_value=0.0, value=float(cur), format="%.8f", key=f"hold_{sym}")
            new_holdings[sym] = float(val)
        submitted = st.form_submit_button("Speichern")
        if submitted:
            # Remove zeros to keep portfolio tidy
            cleaned = {k: v for k, v in new_holdings.items() if v and v > 0}
            st.session_state.holdings = cleaned
            st.success("Holdings gespeichert")

    st.markdown("Aktuelle Holdings:")
    st.json(st.session_state.holdings)

elif menu == "Neue Investition":
    st.header("Neue Investition")
    st.markdown("Betrag in USD eingeben und Coin auswählen. Der Betrag wird in Menge umgerechnet und zum Portfolio hinzugefügt.")
    with st.form("new_inv"):
        amount = st.number_input("Betrag (USD)", min_value=0.01, value=100.0, step=1.0)
        coin = st.selectbox("Coin", COIN_SYMBOLS)
        submit = st.form_submit_button("Investieren")
        if submit:
            price = prices.get(coin, {}).get("price", None)
            if price is None or price == 0:
                st.error("Preis nicht verfügbar. Bitte Preise aktualisieren.")
            else:
                qty = amount / price
                # add to holdings
                cur = st.session_state.holdings.get(coin, 0.0)
                st.session_state.holdings[coin] = cur + qty
                st.success(f"{amount:.2f}$ investiert in {coin} → Menge {qty:.8f} hinzugefügt")
                st.experimental_rerun()

elif menu == "Live Preise":
    st.header("Live Preise (CoinGecko)")
    st.markdown("Aktuelle Preise in USD und 24h Änderung.")
    rows = []
    for sym in COIN_SYMBOLS:
        info = prices.get(sym, {})
        price = info.get("price")
        chg = info.get("change_24h")
        rows.append({
            "Coin": sym,
            "Preis (USD)": f"${price:,.6f}" if price is not None else "N/A",
            "24h %": f"{chg:+.2f}%" if chg is not None else "N/A"
        })
    st.table(pd.DataFrame(rows))

elif menu == "Ziel Simulator":
    st.header("Ziel Simulator")
    st.markdown("Schätze, wie lange es dauert, bis ein Zielbetrag erreicht wird bei monatlichen Einzahlungen und angenommener jährlicher Rendite.")
    with st.form("sim"):
        target = st.number_input("Zielbetrag (USD)", min_value=1.0, value=10000.0, step=100.0)
        monthly = st.number_input("Monatliche Einzahlung (USD)", min_value=0.0, value=200.0, step=10.0)
        current_total = float(pd.DataFrame(portfolio_df(st.session_state.holdings, prices))["Wert (USD)"].sum() or 0.0)
        current = st.number_input("Aktueller Portfolio-Wert (USD)", value=float(current_total), min_value=0.0)
        annual_return = st.number_input("Erwartete jährliche Rendite (%)", min_value=-100.0, value=12.0, step=0.1)
        submit = st.form_submit_button("Berechnen")
        if submit:
            r = annual_return / 100.0
            m_rate = (1 + r) ** (1/12) - 1  # monthly return
            # If monthly contribution is zero, simple growth
            if monthly <= 0:
                if r <= 0:
                    st.info("Mit keiner Einzahlung und nicht-positiver Rendite kann Ziel nicht erreicht werden.")
                else:
                    years = math.log(target / max(1e-9, current)) / math.log(1 + r)
                    st.success(f"Benötigte Zeit: ca. {years:.1f} Jahre")
            else:
                # Use future value formula with monthly contributions and current principal
                # FV = current*(1+m_rate)^n + monthly * [((1+m_rate)^n -1)/m_rate]
                # Solve for n via numeric iteration
                n = 0
                max_months = 1000*12  # safety cap
                cur_val = current
                while n < max_months and cur_val < target:
                    cur_val = current * ((1 + m_rate) ** n) + monthly * (((1 + m_rate) ** n - 1) / (m_rate if m_rate != 0 else 1)) 
                    n += 1
                if n >= max_months:
                    st.info("Ziel in begrenztem Horizont nicht erreichbar (oder sehr weit).")
                else:
                    years = n / 12.0
                    st.success(f"Ungefähr {years:.1f} Jahre ({n} Monate) bis zum Ziel bei {annual_return:.2f}% p.a.")

# --------------------------
# Footer: Disclaimer
# --------------------------
st.markdown("---")
st.caption("APEX Personal — Demo App. Keine Anlageberatung. Preise von CoinGecko.")
