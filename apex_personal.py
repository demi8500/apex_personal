# app.py - APEX Personal (komplett, getestet)
# Passwort: bnc2500
# Benötigt: streamlit, requests, pandas, numpy, plotly

import io
import math
import time
import requests
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="APEX Personal", layout="wide")

# ---------------------
# Styling (dark)
# ---------------------
st.markdown(
    """
    <style>
    .reportview-container, .main, .block-container { background-color: #0b1020; color: #d6e1ff; }
    .stButton>button { background-color: #0f62fe; color: white; }
    input, select, textarea { background-color: #0f1724 !important; color: #d6e1ff !important; border: 1px solid #223 !important; }
    .card { background: #0f1724; padding: 12px; border-radius: 10px; border: 1px solid #233; margin-bottom:12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------
# Coin definitions
# ---------------------
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

# ---------------------
# Utilities: CoinGecko
# ---------------------
def fetch_prices(symbols):
    ids = ",".join(COINS[s] for s in symbols)
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ids, "vs_currencies": "usd", "include_24hr_change": "true"}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    out = {}
    for s in symbols:
        cid = COINS[s]
        entry = data.get(cid, {})
        out[s] = {"price": entry.get("usd"), "change_24h": entry.get("usd_24h_change")}
    return out

def fetch_market_chart(symbol, days=90):
    cid = COINS.get(symbol)
    if not cid:
        return pd.DataFrame(columns=["timestamp", "price"])
    url = f"https://api.coingecko.com/api/v3/coins/{cid}/market_chart"
    params = {"vs_currency": "usd", "days": days, "interval": "hourly" if days <= 90 else "daily"}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    prices = data.get("prices", [])
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

# ---------------------
# Technical: RSI
# ---------------------
def compute_rsi(series, period=14):
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    ma_up = up.ewm(alpha=1/period, adjust=False).mean()
    ma_down = down.ewm(alpha=1/period, adjust=False).mean()
    rs = ma_up / ma_down.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi

# ---------------------
# Session state defaults
# ---------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "holdings" not in st.session_state:
    st.session_state.holdings = {"BTC": 0.02, "ETH": 0.3, "DOGE": 1000, "SHIB": 2000000}
if "last_prices" not in st.session_state:
    st.session_state.last_prices = {}
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = 0
if "rsi_cache" not in st.session_state:
    st.session_state.rsi_cache = {}

# ---------------------
# Simple auth
# ---------------------
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

# ---------------------
# Sidebar menu
# ---------------------
st.sidebar.title("APEX Personal")
menu = st.sidebar.radio("Menü", ["Dashboard", "Trading Signals", "Holdings bearbeiten", "Neue Investition", "Live Preise", "Ziel Simulator"])
if st.sidebar.button("Preise aktualisieren"):
    st.session_state.last_refresh = 0

# ---------------------
# Price caching
# ---------------------
def get_prices_cached():
    now = time.time()
    if now - st.session_state.last_refresh > 10:
        try:
            st.session_state.last_prices = fetch_prices(COIN_SYMBOLS)
            st.session_state.last_refresh = now
        except Exception as e:
            st.error(f"Fehler beim Abrufen der Preise: {e}")
    return st.session_state.last_prices

prices = get_prices_cached()

# ---------------------
# Portfolio helpers
# ---------------------
def portfolio_df(holdings, prices):
    rows = []
    for sym, amt in holdings.items():
        info = prices.get(sym, {})
        p = info.get("price")
        val = p * amt if p is not None else None
        chg = info.get("change_24h")
        rows.append({"Coin": sym, "Menge": amt, "Preis (USD)": p, "Wert (USD)": val, "24h %": chg})
    return pd.DataFrame(rows)

# ---------------------
# Signals (24h-change + RSI)
# ---------------------
def trading_signal_enhanced(change24, rsi):
    if change24 is None:
        base = 0
    else:
        if change24 >= 8:
            base = 2
        elif change24 >= 2:
            base = 1
        elif change24 > -2:
            base = 0
        elif change24 > -8:
            base = -1
        else:
            base = -2
    adj = 0
    if rsi is not None:
        if rsi < 30:
            adj = 1
        elif rsi > 70:
            adj = -1
    score = base + adj
    if score >= 3:
        return "STRONG BUY"
    if score == 2:
        return "BUY"
    if score in (0, 1):
        return "HOLD"
    if score == -1:
        return "SELL"
    return "STRONG SELL"

SIGNAL_COLORS = {
    "STRONG BUY": "#007a3d",
    "BUY": "#0bad4f",
    "HOLD": "#ffc107",
    "SELL": "#ff6b6b",
    "STRONG SELL": "#c62828",
}

# ---------------------
# CSV helpers
# ---------------------
def holdings_to_csv(holdings):
    df = pd.DataFrame(list(holdings.items()), columns=["Coin", "Menge"])
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    buf.seek(0)
    return buf

def csv_to_holdings(uploaded):
    try:
        df = pd.read_csv(uploaded)
        out = {}
        for _, row in df.iterrows():
            coin = str(row.get("Coin", "")).strip().upper()
            if coin in COINS:
                amt = float(row.get("Menge", 0) or 0)
                if amt > 0:
                    out[coin] = amt
        return out
    except Exception:
        return None

# ---------------------
# Pages
# ---------------------
if menu == "Dashboard":
    st.header("Dashboard")
    df = portfolio_df(st.session_state.holdings, prices)
    total_value = df["Wert (USD)"].sum() if not df.empty else 0.0
    denom = df["Wert (USD)"].sum() if not df.empty else 0.0
    if denom and denom > 0:
        weighted_change = (df["Wert (USD)"] * (df["24h %"] / 100.0)).sum()
        pct_change = weighted_change / denom * 100.0
    else:
        pct_change = 0.0

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Gesamtwert")
        st.markdown(f"<h2>${total_value:,.2f}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Portfolio Veränderung (24h geschätzt)")
        color = "#4caf50" if pct_change > 0 else ("#ef5350" if pct_change < 0 else "#d6e1ff")
        st.markdown(f"<h3 style='color:{color}'>{pct_change:+.2f}%</h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### Holdings Übersicht")
    display_df = df.copy()
    display_df["Preis (USD)"] = display_df["Preis (USD)"].map(lambda x: f"${x:,.4f}" if pd.notna(x) else "N/A")
    display_df["Wert (USD)"] = display_df["Wert (USD)"].map(lambda x: f"${x:,.2f}" if pd.notna(x) else "N/A")
    display_df["24h %"] = display_df["24h %"].map(lambda x: f"{x:+.2f}%" if pd.notna(x) else "N/A")
    st.dataframe(display_df, use_container_width=True)

    if not df.empty:
        chart_df = df.dropna(subset=["Wert (USD)"]).sort_values("Wert (USD)", ascending=False).head(10)
        if not chart_df.empty:
            fig = px.pie(chart_df, names="Coin", values="Wert (USD)", title="Top Holdings Verteilung")
            st.plotly_chart(fig, use_container_width=True)

elif menu == "Trading Signals":
    st.header("Trading Signals (24h-change + RSI)")
    st.markdown("Signale kombiniert aus 24h %-Änderung und RSI(14) basierend auf 90d Historie.")

    signals = []
    for sym in COIN_SYMBOLS:
        info = prices.get(sym, {})
        price = info.get("price")
        chg = info.get("change_24h")
        rsi_val = None
        df_hist = pd.DataFrame()
        cached = st.session_state.rsi_cache.get(sym)
        now = time.time()
        if cached and now - cached[0] < 600:
            rsi_val = cached[1]
            df_hist = cached[2]
        else:
            try:
                df_hist = fetch_market_chart(sym, days=90)
                if not df_hist.empty:
                    rsi_series = compute_rsi(df_hist["price"])
                    rsi_val = float(rsi_series.dropna().iloc[-1]) if not rsi_series.dropna().empty else None
                    st.session_state.rsi_cache[sym] = (now, rsi_val, df_hist)
            except Exception:
                rsi_val = None
                df_hist = pd.DataFrame()
        sig = trading_signal_enhanced(chg, rsi_val)
        signals.append((sym, price, chg, rsi_val, sig, df_hist))

    cols = st.columns(3)
    for idx, (sym, price, chg, rsi_val, sig, df_hist) in enumerate(signals):
        c = cols[idx % 3]
        with c:
            color = SIGNAL_COLORS.get(sig, "#222")
            st.markdown(f"<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='margin:0'>{sym}</h4>", unsafe_allow_html=True)
            if price is not None:
                st.markdown(f"<div>Preis: <b>${price:,.4f}</b></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div>Preis: N/A</div>", unsafe_allow_html=True)
            if chg is not None:
                st.markdown(f"<div>24h: {chg:+.2f}%</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div>24h: N/A</div>", unsafe_allow_html=True)
            if rsi_val is not None:
                st.markdown(f"<div>RSI(14): {rsi_val:.1f}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div>RSI(14): N/A</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-top:8px;padding:8px;border-radius:6px;background:{color};color:white;text-align:center'><b>{sig}</b></div>", unsafe_allow_html=True)
            with st.expander("Preisverlauf (90d)"):
                if not df_hist.empty:
                    fig = px.line(df_hist, x="timestamp", y="price", title=f"{sym} Preis (90d)", height=300)
                    st.plotly_chart(fig, use_container_width=True)
                    rsi_series = compute_rsi(df_hist["price"])
                    if not rsi_series.dropna().empty:
                        fig_rsi = px.line(df_hist.assign(RSI=rsi_series), x="timestamp", y="RSI", title=f"{sym} RSI(14)", height=180)
                        st.plotly_chart(fig_rsi, use_container_width=True)
                else:
                    st.info("Historische Daten nicht verfügbar")
            st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Holdings bearbeiten":
    st.header("Holdings bearbeiten")
    st.markdown("Bearbeite Mengen manuell, importiere CSV oder exportiere CSV.")

    uploaded = st.file_uploader("CSV import (Spalten: Coin,Menge)", type=["csv"])
    if uploaded:
        new = csv_to_holdings(uploaded)
        if new is None:
            st.error("CSV konnte nicht gelesen werden. Format prüfen.")
        else:
            if st.checkbox("Ersetze bestehende Holdings mit CSV"):
                st.session_state.holdings = new
                st.success("Holdings ersetzt mit CSV")
            else:
                for k, v in new.items():
                    st.session_state.holdings[k] = st.session_state.holdings.get(k, 0.0) + v
                st.success("CSV-Holdings hinzugefügt")

    with st.form("edit_holdings"):
        new_holdings = {}
        for sym in COIN_SYMBOLS:
            cur = st.session_state.holdings.get(sym, 0.0)
            val = st.number_input(f"{sym} Menge", min_value=0.0, value=float(cur), format="%.8f", key=f"hold_{sym}")
            new_holdings[sym] = float(val)
        submitted = st.form_submit_button("Speichern")
        if submitted:
            cleaned = {k: v for k, v in new_holdings.items() if v and v > 0}
            st.session_state.holdings = cleaned
            st.success("Holdings gespeichert")

    st.markdown("Aktuelle Holdings:")
    st.json(st.session_state.holdings)

    buf = holdings_to_csv(st.session_state.holdings)
    st.download_button("Export CSV", buf, file_name="holdings.csv", mime="text/csv")

elif menu == "Neue Investition":
    st.header("Neue Investition")
    st.markdown("Betrag in USD eingeben und Coin auswählen → Menge wird berechnet und zum Portfolio hinzugefügt.")
    with st.form("new_inv"):
        amount = st.number_input("Betrag (USD)", min_value=0.01, value=100.0, step=1.0)
        coin = st.selectbox("Coin", COIN_SYMBOLS)
        submit = st.form_submit_button("Investieren")
        if submit:
            price = prices.get(coin, {}).get("price")
            if not price:
                st.error("Preis nicht verfügbar. Preise aktualisieren.")
            else:
                qty = amount / price
                st.session_state.holdings[coin] = st.session_state.holdings.get(coin, 0.0) + qty
                st.success(f"{amount:.2f}$ investiert in {coin} → +{qty:.8f} {coin}")
                st.experimental_rerun()

elif menu == "Live Preise":
    st.header("Live Preise (CoinGecko)")
    st.markdown("Aktuelle Preise in USD und 24h Änderung.")
    rows = []
    for sym in COIN_SYMBOLS:
        info = prices.get(sym, {})
        price = info.get("price")
        chg = info.get("change_24h")
        rows.append({"Coin": sym, "Preis (USD)": f"${price:,.6f}" if price is not None else "N/A",
                     "24h %": f"{chg:+.2f}%" if chg is not None else "N/A"})
    st.table(pd.DataFrame(rows))

elif menu == "Ziel Simulator":
    st.header("Ziel Simulator")
    st.markdown("Schätzt Jahre bis Ziel bei monatlichen Einzahlungen und erwarteter Rendite.")
    with st.form("sim"):
        target = st.number_input("Zielbetrag (USD)", min_value=1.0, value=10000.0, step=100.0)
        monthly = st.number_input("Monatliche Einzahlung (USD)", min_value=0.0, value=200.0, step=10.0)
        current_total = float(portfolio_df(st.session_state.holdings, prices)["Wert (USD)"].sum() or 0.0)
        current = st.number_input("Aktueller Portfolio-Wert (USD)", value=float(current_total), min_value=0.0)
        annual_return = st.number_input("Erwartete jährliche Rendite (%)", min_value=-100.0, value=12.0, step=0.1)
        submit = st.form_submit_button("Berechnen")
        if submit:
            r = annual_return / 100.0
            m_rate = (1 + r) ** (1/12) - 1
            if monthly <= 0:
                if r <= 0:
                    st.info("Kein Wachstum ohne Einzahlung und nicht-positiver Rendite.")
                else:
                    years = math.log(target / max(1e-9, current)) / math.log(1 + r)
                    st.success(f"Benötigte Zeit: ca. {years:.1f} Jahre")
            else:
                n = 0
                max_months = 1000 * 12
                cur_val = current
                while n < max_months and cur_val < target:
                    if m_rate != 0:
                        cur_val = current * ((1 + m_rate) ** n) + monthly * (((1 + m_rate) ** n - 1) / m_rate)
                    else:
                        cur_val = current + monthly * n
                    n += 1
                if n >= max_months:
                    st.info("Ziel in begrenztem Horizont nicht erreichbar (oder sehr weit).")
                else:
                    years = n / 12.0
                    st.success(f"Ungefähr {years:.1f} Jahre ({n} Monate) bis zum Ziel bei {annual_return:.2f}% p.a.")

st.markdown("---")
st.caption("APEX Personal — Demo App. Keine Anlageberatung. Preise von CoinGecko.")
