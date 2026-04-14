import yfinance as yf

from tools.finance import ACTIONS


def _recuperer_cours_et_reference(symbole_yf: str) -> tuple[float, float]:
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
        previous_close = close

    return close, previous_close


def calculer_valeur_portefeuille(input_str: str) -> str:
    """
    Calcule la valeur d'un portefeuille d'actions.
    Entrée : "SYMBOLE:QUANTITE|SYMBOLE:QUANTITE"
    Exemple : "AAPL:10|MSFT:4|LVMH:2"
    """
    try:
        positions = []
        for bloc in input_str.strip().split("|"):
            bloc = bloc.strip()
            if not bloc:
                continue
            if ":" not in bloc:
                return (
                    "Format invalide. Utilisez : SYMBOLE:QUANTITE|SYMBOLE:QUANTITE "
                    "(ex: AAPL:10|MSFT:5)."
                )

            symbole, quantite = bloc.split(":", 1)
            symbole = symbole.strip().upper()
            quantite = float(quantite.strip().replace(",", "."))

            if not symbole or quantite <= 0:
                return "Format invalide. Quantité strictement positive requise pour chaque ligne."

            positions.append((symbole, quantite))

        if not positions:
            return "Aucune position valide fournie."

        lignes = []
        total_actuel = 0.0
        total_reference = 0.0
        symboles_invalides = []

        for symbole, quantite in positions:
            symbole_yf = ACTIONS.get(symbole, symbole)
            try:
                close, previous_close = _recuperer_cours_et_reference(symbole_yf)
            except ValueError:
                symboles_invalides.append(symbole)
                continue

            valeur_actuelle = close * quantite
            valeur_reference = previous_close * quantite
            variation_abs = valeur_actuelle - valeur_reference
            variation_pct = (
                ((close - previous_close) / previous_close) * 100
                if previous_close != 0
                else 0.0
            )

            total_actuel += valeur_actuelle
            total_reference += valeur_reference

            lignes.append(
                f"- {symbole} x{quantite:g} | Cours : {close:.2f} $ | Valeur : {valeur_actuelle:.2f} $ "
                f"| Var jour : {variation_pct:+.2f}% ({variation_abs:+.2f} $)"
            )

        if not lignes:
            return (
                "Aucune donnée récupérable pour les symboles fournis. "
                "Vérifiez les symboles (ex: AAPL, MSFT, TSLA, LVMH)."
            )

        variation_totale_abs = total_actuel - total_reference
        variation_totale_pct = (
            (variation_totale_abs / total_reference) * 100
            if total_reference != 0
            else 0.0
        )

        resultat = "Valeur du portefeuille :\n"
        resultat += "\n".join(lignes)
        resultat += (
            f"\nTotal portefeuille : {total_actuel:.2f} $"
            f"\nVariation globale du jour : {variation_totale_pct:+.2f}% ({variation_totale_abs:+.2f} $)"
        )

        if symboles_invalides:
            resultat += "\nSymboles ignorés (introuvables) : " + ", ".join(
                symboles_invalides
            )

        return resultat
    except ValueError:
        return (
            "Format invalide. Utilisez : SYMBOLE:QUANTITE|SYMBOLE:QUANTITE "
            "(ex: AAPL:10|MSFT:5)."
        )
    except Exception:
        return "Service financier indisponible pour le moment (portefeuille)."


if __name__ == "__main__":
    print(calculer_valeur_portefeuille("AAPL:10|MSFT:5|LVMH:2"))
