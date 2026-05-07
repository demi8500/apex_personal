# app.py - APEX Personal (sauber, funktionierend)
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
    if series is None or series.empty:
        return pd.Series(dtype=float)
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    ma_up = up.ewm(alpha=1/period, adjust=False).mean()
    ma_down = down.ewm(alpha=1/period, adjust=False).mean()
    rs = ma_up / ma_down.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi

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
                try:
                    amt = float(row.get("Menge", 0) or 0)
                except Exception:
                    amt = 0.0
                if amt > 0:
                    out[coin] = amt
        return out
    except Exception:
        return None

# ---------------------
# Portfolio & signals helpers
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

def trading_signal_enhanced(change24, rsi):
    if change24 is None:
        base = 0
    else:
        if change24 >= 8:
            base = 2
    
