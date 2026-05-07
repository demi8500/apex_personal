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
