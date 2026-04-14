from typing import TypedDict

import yfinance as yf


class Quote(TypedDict):
    close: float
    variation_pct: float
    volume: int


ACTIONS = {
    "AAPL": "AAPL",
    "MSFT": "MSFT",
    "GOOGL": "GOOGL",
    "LVMH": "MC.PA",
    "TSLA": "TSLA",
    "AIR": "AIR.PA",
}

CRYPTOS = {
    "BTC": "BTC-USD",
    "ETH": "ETH-USD",
    "SOL": "SOL-USD",
    "BNB": "BNB-USD",
    "DOGE": "DOGE-USD",
}


def _recuperer_quote(symbole_yf: str) -> Quote:
    ticker = yf.Ticker(symbole_yf)
    history = ticker.history(period="5d", interval="1d", auto_adjust=False)

    if history.empty:
        raise ValueError("Aucune donnee de marche disponible pour ce symbole.")

    close_series = history["Close"].dropna()
    if close_series.empty:
        raise ValueError("Cours indisponible pour ce symbole.")

    close = float(close_series.iloc[-1])

    previous_close = None
    try:
        fast_info = ticker.fast_info
        previous_close = float(fast_info.get("previousClose"))
    except Exception:
        previous_close = None

    if previous_close in (None, 0.0) and len(close_series) > 1:
        previous_close = float(close_series.iloc[-2])

    if previous_close in (None, 0.0):
        variation_pct = 0.0
    else:
        variation_pct = ((close - previous_close) / previous_close) * 100

    volume_series = history["Volume"].dropna()
    volume = int(volume_series.iloc[-1]) if not volume_series.empty else 0

    return {
        "close": close,
        "variation_pct": variation_pct,
        "volume": volume,
    }


def obtenir_cours_action(symbole: str) -> str:
    """Retourne le cours reel d'une action avec variation du jour et volume."""
    symbole = symbole.strip().upper()
    symbole_yf = ACTIONS.get(symbole, symbole)

    try:
        quote = _recuperer_quote(symbole_yf)
    except ValueError:
        return f"Action '{symbole}' non trouvée."
    except Exception:
        return "Service financier indisponible pour le moment (actions)."

    tendance = "📈" if quote["variation_pct"] >= 0 else "📉"
    return (
        f"{symbole} {tendance} : {quote['close']:.2f} $ ({quote['variation_pct']:+.2f}%) "
        f"| Volume : {quote['volume']:,}"
    )


def obtenir_cours_crypto(symbole: str) -> str:
    """Retourne le cours reel d'une crypto avec variation du jour et volume."""
    symbole = symbole.strip().upper()
    if "-" in symbole:
        symbole_yf = symbole
        symbole_affiche = symbole.split("-")[0]
    else:
        symbole_yf = CRYPTOS.get(symbole, f"{symbole}-USD")
        symbole_affiche = symbole

    try:
        quote = _recuperer_quote(symbole_yf)
    except ValueError:
        return f"Crypto '{symbole_affiche}' non trouvée."
    except Exception:
        return "Service financier indisponible pour le moment (cryptos)."

    tendance = "📈" if quote["variation_pct"] >= 0 else "📉"
    return (
        f"{symbole_affiche} {tendance} : {quote['close']:.2f} $ ({quote['variation_pct']:+.2f}%) "
        f"| Volume : {quote['volume']:,}"
    )


if __name__ == "__main__":
    print("== test finance ==")
    print(obtenir_cours_action("AAPL"))
    print(obtenir_cours_action("LVMH"))
    print(obtenir_cours_action("INVALID"))
    print(obtenir_cours_crypto("BTC"))
