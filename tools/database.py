import os
from typing import Any

try:
    import psycopg
    from psycopg import Error as PsycopgError
    from psycopg.rows import dict_row

    _PSYCOPG_IMPORT_ERROR: Exception | None = None
except ImportError as exc:
    psycopg = None
    dict_row = None
    PsycopgError = Exception
    _PSYCOPG_IMPORT_ERROR = exc


def _connect_db() -> Any:
    if psycopg is None or dict_row is None:
        raise RuntimeError(
            "psycopg indisponible (libpq manquante). "
            "Installez libpq ou psycopg[binary]."
        ) from _PSYCOPG_IMPORT_ERROR

    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", os.getenv("DB_HOST", "localhost")),
        port=int(os.getenv("POSTGRES_PORT", os.getenv("DB_PORT", "5432"))),
        dbname=os.getenv("POSTGRES_DB", "vectordb"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        connect_timeout=int(os.getenv("POSTGRES_CONNECT_TIMEOUT", "5")),
        row_factory=dict_row,
    )


def _fetch_one(sql: str, params: tuple[Any, ...]) -> dict[str, Any] | None:
    with _connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone()


def rechercher_client(query: str) -> str:
    """Recherche un client par nom ou par identifiant."""
    query = query.strip()
    if not query:
        return "Aucun client trouvé pour : ''"

    try:
        client = _fetch_one(
            """
            SELECT nom, solde_compte, type_compte
            FROM clients
            WHERE id_client = %s
            """,
            (query.upper(),),
        )

        if client is None:
            client = _fetch_one(
                """
                SELECT nom, solde_compte, type_compte
                FROM clients
                WHERE nom ILIKE %s
                ORDER BY id_client
                LIMIT 1
                """,
                (f"%{query}%",),
            )

        if client is None:
            return f"Aucun client trouvé pour : '{query}'"

        return (
            f"Client : {client['nom']} | Solde : {client['solde_compte']:.2f} € "
            f"| Type de compte : {client['type_compte']}"
        )
    except (PsycopgError, RuntimeError) as exc:
        return f"Erreur base de données (clients) : {exc.__class__.__name__}"


def rechercher_produit(query: str) -> str:
    """Recherche un produit par nom ou identifiant. Retourne prix HT, TVA, prix TTC, stock."""
    query = query.strip()
    if not query:
        return "Aucun produit trouvé pour : ''"

    try:
        produit = _fetch_one(
            """
            SELECT nom, prix_ht, stock
            FROM produits
            WHERE id_produit = %s
            """,
            (query.upper(),),
        )

        if produit is None:
            produit = _fetch_one(
                """
                SELECT nom, prix_ht, stock
                FROM produits
                WHERE nom ILIKE %s
                ORDER BY id_produit
                LIMIT 1
                """,
                (f"%{query}%",),
            )

        if produit is None:
            return f"Aucun produit trouvé pour : '{query}'"

        tva = produit["prix_ht"] * 0.20
        prix_ttc = produit["prix_ht"] + tva
        return (
            f"Produit : {produit['nom']} | Prix HT : {produit['prix_ht']:.2f} € "
            f"| TVA : {tva:.2f} € | Prix TTC : {prix_ttc:.2f} € | Stock : {produit['stock']}"
        )
    except (PsycopgError, RuntimeError) as exc:
        return f"Erreur base de données (produits) : {exc.__class__.__name__}"


def lister_tous_les_clients(query: str = "") -> str:
    """Retourne la liste complète de tous les clients."""
    try:
        with _connect_db() as conn:
            rows = conn.execute(
                """
                SELECT id_client, nom, type_compte, solde_compte
                FROM clients
                ORDER BY id_client
                """
            ).fetchall()

        result = "Liste des clients :\n"
        for row in rows:
            result += (
                f"  {row['id_client']} : {row['nom']} | {row['type_compte']} "
                f"| Solde : {row['solde_compte']:.2f} €\n"
            )
        return result
    except (PsycopgError, RuntimeError) as exc:
        return f"Erreur base de données (liste clients) : {exc.__class__.__name__}"
