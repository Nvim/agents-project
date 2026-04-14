import random

ACTIONS = {
    "AAPL":  { "nom": "Apple Inc.",       "prix_base": 182.50 },
    "MSFT":  { "nom": "Microsoft Corp.",   "prix_base": 415.20 },
    "GOOGL": { "nom": "Alphabet (Google)", "prix_base": 175.80 },
    "LVMH":  { "nom": "LVMH Moët Hennessy","prix_base": 750.00 },
    "TSLA":  { "nom": "Tesla Inc.",         "prix_base": 248.00 },
    "AIR":   { "nom": "Airbus SE",          "prix_base": 168.40 },
}
 
CRYPTOS = {
    "BTC": { "nom": "Bitcoin",  "prix_base": 67500.00 },
    "ETH": { "nom": "Ethereum", "prix_base": 3200.00  },
    "SOL": { "nom": "Solana",   "prix_base": 175.00   },
}
 
def obtenir_cours_action(symbole: str) -> str:
    """Retourne le cours simulé d'une action avec sa variation (+/-3%)."""
    symbole = symbole.strip().upper()
    if symbole not in ACTIONS:
        return f"Action '{symbole}' non trouvée."
    action = ACTIONS[symbole]
    variation_pct = random.uniform(-3.0, 3.0)   # Variation aléatoire
    cours = action['prix_base'] * (1 + variation_pct / 100)
    tendance = '📈' if variation_pct >= 0 else '📉'
    return f"{symbole} {tendance} : {cours:.2f} $ ({variation_pct:+.2f}%)"

if __name__ == "__main__":
    print("== test finance ==")
    print(obtenir_cours_action("AAPL"))
    print(obtenir_cours_action("LVMH"))
    print(obtenir_cours_action("INVALID"))

def obtenir_cours_crypto(symbole: str) -> str:
    """Retourne le cours simulé d'une crypto avec sa variation (+/-3%)."""
    symbole = symbole.strip().upper()
    if symbole not in CRYPTOS:
        return f"Crypto '{symbole}' non trouvée."
    crypto = CRYPTOS[symbole]
    variation_pct = random.uniform(-30.0, 30.0)   # Variation aléatoire
    cours = crypto['prix_base'] * (1 + variation_pct / 100)
    tendance = '📈' if variation_pct >= 0 else '📉'
    return f"{symbole} {tendance} : {cours:.2f} $ ({variation_pct:+.2f}%)"
