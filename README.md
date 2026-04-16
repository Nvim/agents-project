# Agent LangChain Python (Projet TP)

Agent conversationnel financier basé sur LangChain avec outils métier (base clients/produits, finance temps réel, recommandation, conversion devise, recherche web, Python REPL, etc.).

## Prérequis

- Python `3.12`
- `docker` + `docker compose`
- Environnement virtuel `.venv` du projet (obligatoire)

## 1) Configuration

Créer le fichier d'environnement local à partir de l'exemple :

```bash
cp .env.example .env
```

Renseigner au minimum :

- `OPENAI_API_KEY`
- `TAVILY_API_KEY`

## 2) Démarrer PostgreSQL

Lancer la base:

```bash
docker compose up -d
```

La base est initialisée automatiquement via `db/database.db.sql` au premier démarrage du volume.

Si vous devez réinitialiser les données :

```bash
docker compose down -v
docker compose up -d
```

## 3) Installer les dépendances (si nécessaire)

```bash
.venv/bin/python -m pip install -r requirements.txt
```

## 4) Lancer l'agent en CLI

```bash
.venv/bin/python main.py
```

Le menu propose des scénarios de démonstration (BDD, finance réelle, Tavily, portefeuille, mémoire conversationnelle, etc.).

## 5) Lancer l'interface Streamlit (C1)

```bash
.venv/bin/streamlit run app.py
```

Fonctionnalités : historique de conversation, champ de saisie en bas de page, sidebar des outils, bouton de réinitialisation.

## Variables d'environnement

Variables principales utilisées par le projet :

- `OPENAI_API_KEY` : clé API OpenAI
- `TAVILY_API_KEY` : clé API Tavily (outil web)
- `POSTGRES_HOST` (défaut `localhost`)
- `POSTGRES_PORT` (défaut `5432`)
- `POSTGRES_DB` (défaut `vectordb`)
- `POSTGRES_USER` (défaut `postgres`)
- `POSTGRES_PASSWORD` (défaut `postgres`)
- `POSTGRES_CONNECT_TIMEOUT` (défaut `5`)

## Notes techniques

- Les outils `rechercher_client` et `rechercher_produit` sont en `return_direct` pour éviter un fallback (ex: websearch) si la base est indisponible.
- Le tool `python_repl` exécute du code arbitraire (danger en production sans sandbox).
