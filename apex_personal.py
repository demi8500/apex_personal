# apex_personal.py
# APEX Personal - Single-file Streamlit app
# Requirements:
# - Passwortschutz (Passwort: "bnc2500")
# - Dunkles modernes Design
# - Sidebar Menü: Dashboard, Trading Signals, Holdings bearbeiten, Neue Investition, Live Preise, Ziel Simulator
# - CoinGecko API für Live-Preise
# - Lokale Speicherung der Holdings in holdings.json
# - Sauber, verständlich kommentiert

import streamlit as st
import requests
import json
import os
from datetime import datetime
from math import log, ceil

# --------------------
# Konfiguration
# --------------------
APP_TITLE = "APEX Personal"
PASSWORD = "bnc2500"
HOLDINGS_FILE = "holdings.json"
COINS = [
    "bitcoin", "ethereum", "solana", "binancecoin", "ripple",  # BTC, ETH, SOL, BNB, XRP
    "dogecoin", "shiba-inu", "pepe", "bonk", "wif", "floki",   # DOGE, SHIB, PEPE, BONK, WIF, FLOKI
    "cardano", "avalanche-2", "chainlink", "toncoin"           # ADA, AVAX, LINK, TON
]
# Kurzbezeichnungen (für Anzeige)
COIN_SYMBOLS = {
    "bitcoin": "BTC", "ethereum": "ETH", "solana": "SOL", "binancecoin": "BNB", "ripple": "XRP",
    "dogecoin": "DOGE", "shiba-inu": "SHIB", "pepe": "PEPE", "bonk": "BONK", "wif": "WIF", "floki": "FLOKI",
    "cardano": "ADA", "avalanche-2": "AVAX", "chainlink": "LINK", "toncoin": "TON"
}
VS_CURRENCY = "usd"  # Preise in USD

# --------------------
# Hilfsfunktionen
# --------------------

def init_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "holdings" not in st.session_state:
        st.session_state.holdings = load_holdings()
    if "prices" not in st.session_state:
        st.session_state.prices = {}

def load_holdings():
    # Lade Holdings von Datei oder initialisiere leere Struktur (alle Coins mit 0)
    if os.path.exists(HOLDINGS_FILE):
        try:
            with open(HOLDINGS_FILE, "r") as f:
                data = json.load(f)
            # Sicherstellen, dass alle Coins vorhanden sind
            for c in COINS:
                if c not in data:
                    data[c] = 0.0
            return data
        except Exception:
            pass
    # Standard: alle 0
    return {c: 0.0 for c in COINS}

def save_holdings():
    try:
        with open(HOLDINGS_FILE, "w") as f:
            json.dump(st.session_state.holdings, f, indent=2)
    except Exception as e:
        st.error(f"Fehler beim Speichern: {e}")

def fetch_prices(ids):
    # CoinGecko simple price endpoint
    ids_str = ",".join(ids)
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ids_str, "vs_currencies": VS_CURRENCY, "include_24hr_change": "true"}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        # Ensure keys exist for all ids
        prices = {}
        for cid in ids:
            if cid in data:
                prices[cid] = {
                    "price": data[cid].get(VS_CURRENCY, None),
                    "change_24h": data[cid].get(f"{VS_CURRENCY}_24h_change", 0.0)
                }
            else:
                prices[cid] = {"price": None, "change_24h": 0.0}
        return prices
    except Exception as e:
        st.error(f"Fehler beim Abrufen der Preise: {e}")
        return {cid: {"price": None, "change_24h": 0.0} for cid in ids}

def compute_portfolio_value(holdings, prices):
    total = 0.0
    per_coin = {}
    for c, amt in holdings.items():
        price = prices.get(c, {}).get("price")
        value = (price or 0.0) * amt
        per_coin[c] = {"amount": amt, "price": price or 0.0, "value": value}
        total += value
    return total, per_coin

def signal_from_change(change_pct):
    # Einfache Signallogik basierend auf 24h Veränderung
    # thresholds (kann angepasst werden)
    if change_pct is None:
        return "HOLD"
    if change_pct >= 10:
        return "STRONG BUY"
    if change_pct >= 2:
        return "BUY"
    if change_pct <= -10:
        return "STRONG SELL"
    if change_pct <= -2:
        return "SELL"
    return "HOLD"

def years_to_target(current, monthly, target, annual_return=0.12):
    # Berechne Jahre bis Ziel mit monatlichen Einzahlungen und angenommener jährlicher Rendite
    # Formel: Future value of a series + current growth. Iterative simulate if needed.
    if monthly <= 0 and current <= 0:
        return float("inf")
    r_month = (1 + annual_return) ** (1/12) - 1
    fv_current = current
    months = 0
    # safety cap
    while fv_current < target and months < 1000:
        # monthly contribution at start of period
        fv_current = fv_current * (1 + r_month) + monthly
        months += 1
    return months / 12.0 if months < 1000 else float("inf")

# --------------------
# UI: Theme / Layout
# --------------------
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")
# Minimaler Dark Style über CSS
st.markdown(
    """
    <style>
    /* dunkles Farbschema */
    .stApp { background-color: #0f1720; color: #e6eef8; }
    .css-1d391kg { color: #e6eef8; } /* some text */
    .stButton>button { background-color: #0ea5a5; color: white; }
    .stSidebar { background-color:#071023; color: #e6eef8; }
    .card { background-color: #0b1220; padding: 12px; border-radius: 8px; margin-bottom: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.5); }
    .signal-buy { background: linear-gradient(90deg,#064e3b,#10b981); color: white; padding:8px; border-radius:6px; }
    .signal-sell { background: linear-gradient(90deg,#7f1d1d,#ef4444); color: white; padding:8px; border-radius:6px; }
    .signal-hold { background: linear-gradient(90deg,#334155,#64748b); color: white; padding:8px; border-radius:6px; }
    table { color: #e6eef8; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------
# Authentifizierung
# --------------------
init_session()

if not st.session_state.authenticated:
    st.title(APP_TITLE)
    st.write("Bitte Passwort eingeben, um die App zu verwenden.")
    pwd = st.text_input("Passwort", type="password")
    if st.button("Anmelden"):
        if pwd == PASSWORD:
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.error("Falsches Passwort.")
    # Stop further render until authenticated
    st.stop()

# --------------------
# Hauptsidebar Menu
# --------------------
st.sidebar.title(APP_TITLE)
menu = st.sidebar.radio("Menü", ["Dashboard", "Trading Signals", "Holdings bearbeiten", "Neue Investition", "Live Preise", "Ziel Simulator"])

# Button zum Ausloggen (setzt Auth zurück)
if st.sidebar.button("Abmelden"):
    st.session_state.authenticated = False
    st.experimental_rerun()

# Aktualisiere Preise (kann manuell getriggert werden)
if st.sidebar.button("Preise aktualisieren"):
    st.session_state.prices = fetch_prices(COINS)

# Falls noch keine Preise geladen: lade initial
if not st.session_state.prices:
    st.session_state.prices = fetch_prices(COINS)

prices = st.session_state.prices
holdings = st.session_state.holdings

# --------------------
# Menü-Implementierungen
# --------------------

if menu == "Dashboard":
    st.header("Dashboard")
    total, per_coin = compute_portfolio_value(holdings, prices)
    # Gesamtwert und prozentuale Veränderung (basierend auf 24h)
    # Näherungsweise Veränderung = gewichteter 24h change
    weighted_change = 0.0
    if total > 0:
        for c, info in per_coin.items():
            pct = prices.get(c, {}).get("change_24h", 0.0) or 0.0
            weighted_change += info["value"] * pct / 100.0
        perc_change = (weighted_change / total) * 100.0
    else:
        perc_change = 0.0

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Gesamtwert")
        st.markdown(f"<div class='card'><h2>${total:,.2f}</h2><p>24h Veränderung: {perc_change:+.2f}%</p></div>", unsafe_allow_html=True)
    with col2:
        st.subheader("Letzte Aktualisierung")
        st.write(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))

    st.subheader("Holdings Übersicht")
    # Tabelle mit Coin, Menge, aktueller Preis, Wert $
    rows = []
    for c, info in per_coin.items():
        rows.append({
            "Coin": COIN_SYMBOLS.get(c, c),
            "Menge": f"{info['amount']:.6f}",
            "Preis (USD)": f"${info['price']:.4f}",
            "Wert (USD)": f"${info['value']:,.2f}"
        })
    st.table(rows)

elif menu == "Trading Signals":
    st.header("Trading Signals")
    st.write("Einfache Signale basierend auf 24h Veränderung.")
    # Karten mit farbiger Darstellung
    cols = st.columns(3)
    i = 0
    for c in COINS:
        sig = signal_from_change(prices.get(c, {}).get("change_24h"))
        price = prices.get(c, {}).get("price")
        change = prices.get(c, {}).get("change_24h", 0.0)
        container = cols[i % 3]
        if sig in ("BUY", "STRONG BUY"):
            cls = "signal-buy"
        elif sig in ("SELL", "STRONG SELL"):
            cls = "signal-sell"
        else:
            cls = "signal-hold"
        with container:
            st.markdown(f"<div class='card {cls}'><b>{COIN_SYMBOLS.get(c,c)}</b><br> {sig} <br>Preis: ${price if price else 'N/A'} <br>24h: {change:+.2f}%</div>", unsafe_allow_html=True)
        i += 1

elif menu == "Holdings bearbeiten":
    st.header("Holdings bearbeiten")
    st.write("Gebe die Menge für jeden Coin ein und speichere.")
    changed = False
    with st.form("edit_holdings"):
        new_holdings = {}
        for c in COINS:
            amt = st.number_input(f"{COIN_SYMBOLS.get(c,c)} Menge", min_value=0.0, value=float(holdings.get(c, 0.0)), format="%.8f", key=f"hold_{c}")
            new_holdings[c] = amt
        submitted = st.form_submit_button("Speichern")
        if submitted:
            st.session_state.holdings = new_holdings
            save_holdings()
            st.success("Holdings gespeichert.")
            st.experimental_rerun()

elif menu == "Neue Investition":
    st.header("Neue Investition")
    st.write("Betrag in USD eingeben und Coin auswählen. Fügt automatisch Menge zum Portfolio hinzu.")
    coin_choice = st.selectbox("Coin", COINS, format_func=lambda x: COIN_SYMBOLS.get(x, x))
    amount_usd = st.number_input("Betrag (USD)", min_value=0.0, step=10.0, value=100.0)
    if st.button("Investieren"):
        price = prices.get(coin_choice, {}).get("price")
        if not price or price == 0:
            st.error("Preis nicht verfügbar. Bitte Preise aktualisieren.")
        else:
            added_amount = amount_usd / price
            st.session_state.holdings[coin_choice] = st.session_state.holdings.get(coin_choice, 0.0) + added_amount
            save_holdings()
            st.success(f"Investiert ${amount_usd:.2f} in {COIN_SYMBOLS.get(coin_choice)} → {added_amount:.6f} {COIN_SYMBOLS.get(coin_choice)} hinzugefügt.")
            st.experimental_rerun()

elif menu == "Live Preise":
    st.header("Live Preise")
    st.write("Aktuelle Preise von CoinGecko. Klick 'Preise aktualisieren' in der Sidebar, um neu zu laden.")
    # Tabelle aller Preise
    price_rows = []
    for c in COINS:
        p = prices.get(c, {}).get("price")
        ch = prices.get(c, {}).get("change_24h", 0.0)
        price_rows.append({
            "Coin": COIN_SYMBOLS.get(c, c),
            "Preis (USD)": f"${p:.6f}" if p else "N/A",
            "24h %": f"{ch:+.2f}%"
        })
    st.table(price_rows)

elif menu == "Ziel Simulator":
    st.header("Ziel Simulator")
    st.write("Gib aktuellen Zielbetrag ein und deine monatliche Einzahlung. Simulation mit angenommener Rendite (Standard 12% p.a.).")
    col1, col2 = st.columns(2)
    with col1:
        target = st.number_input("Zielbetrag (USD)", min_value=0.0, value=100000.0)
        monthly = st.number_input("Monatliche Einzahlung (USD)", min_value=0.0, value=500.0)
    with col2:
        current_total, _ = compute_portfolio_value(holdings, prices)
        st.write(f"Aktuelles Portfolio: ${current_total:,.2f}")
        annual_return = st.number_input("Erwartete jährliche Rendite (%)", min_value=0.0, value=12.0) / 100.0

    if st.button("Berechnen"):
        years = years_to_target(current_total, monthly, target, annual_return)
        if years == float("inf"):
            st.warning("Mit den gegebenen Werten wird das Ziel vermutlich nie erreicht.")
        else:
            years_int = int(years)
            months_rem = int(round((years - years_int) * 12))
            st.success(f"Ungefähr {years:.1f} Jahre (~{years_int} Jahre und {months_rem} Monate) bis zum Ziel bei {annual_return*100:.1f}% p.a.")

# --------------------
# Footer: einfache Hilfe
# --------------------
st.markdown("---")
st.caption("APEX Personal • Preise via CoinGecko • Lokale Speicherung der Holdings in holdings.json")
