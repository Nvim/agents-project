import os
import ast
import contextlib
import io

from langchain_community.tools import TavilySearchResults
from langchain_classic import hub
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_classic.tools import Tool
from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI
from tools.calculations import (
    calculer_interets_composes,
    calculer_marge,
    calculer_mensualite_pret,
    calculer_tva,
)
from tools.database import rechercher_client, rechercher_produit
from tools.finance import obtenir_cours_action, obtenir_cours_crypto
from tools.portefeuille import calculer_valeur_portefeuille
from tools.public_api import convertir_devise
from tools.recommendation import recommander_produits
from tools.text import extraire_mots_cles, formater_rapport, resumer_texte


def _recherche_web_indisponible(_query: str) -> str:
    return (
        "Recherche web indisponible : TAVILY_API_KEY manquant ou configuration invalide. "
        "Ajoutez une clé Tavily valide dans l'environnement."
    )


def _nettoyer_code_python(raw_code: str) -> str:
    code = raw_code.strip()
    if code.startswith("```"):
        lines = code.splitlines()
        if lines:
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        code = "\n".join(lines).strip()
    return code


def _executer_code_python(code: str, python_repl_tool: PythonREPLTool) -> str:
    code = _nettoyer_code_python(code)
    if not code:
        return "Aucun code Python fourni."

    try:
        module = ast.parse(code, mode="exec")
    except SyntaxError as exc:
        return f"Erreur Python : SyntaxError: {exc}"

    repl_globals = python_repl_tool.python_repl.globals
    repl_locals = python_repl_tool.python_repl.locals or repl_globals

    try:
        if module.body and isinstance(module.body[-1], ast.Expr):
            prefix_module = ast.Module(body=module.body[:-1], type_ignores=[])
            expression = ast.Expression(module.body[-1].value)

            stdout_buffer = io.StringIO()
            with contextlib.redirect_stdout(stdout_buffer):
                if prefix_module.body:
                    exec(
                        compile(prefix_module, "<python_repl>", "exec"),
                        repl_globals,
                        repl_locals,
                    )
                value = eval(
                    compile(expression, "<python_repl>", "eval"),
                    repl_globals,
                    repl_locals,
                )

            stdout = stdout_buffer.getvalue().strip()
            value_text = "" if value is None else str(value)
            if stdout and value_text:
                return f"{stdout}\n{value_text}"
            if stdout:
                return stdout
            if value_text:
                return value_text
            return "Code exécuté sans sortie."

        output = python_repl_tool.run(code)
        output_text = "" if output is None else str(output).strip()
        return output_text or "Code exécuté sans sortie."
    except Exception as exc:
        return f"Erreur Python : {exc.__class__.__name__}: {exc}"


def creer_tools():
    """Construit la liste des outils disponibles pour l'agent."""
    tools = [
        # ── Outil 1 : Base de données ─────────────────────────────────────
        Tool(
            name="rechercher_client",
            func=rechercher_client,
            description="Recherche un client par nom ou ID (ex: C001). "
            "Retourne solde, type de compte, historique achats.",
        ),
        Tool(
            name="rechercher_produit",
            func=rechercher_produit,
            description="Recherche un produit par nom ou ID. "
            "Retourne prix HT, TVA, prix TTC, stock.",
        ),
        # ── Outil 2 : Données financières ─────────────────────────────────
        Tool(
            name="cours_action",
            func=obtenir_cours_action,
            description="Cours boursier réel d'une action (Yahoo Finance), avec variation du jour et volume. "
            "Entrée : symbole majuscule ex AAPL, MSFT, TSLA, LVMH, AIR.",
        ),
        Tool(
            name="cours_crypto",
            func=obtenir_cours_crypto,
            description="Cours réel d'une crypto (Yahoo Finance), avec variation du jour et volume. "
            "Entrée : symbole ex BTC, ETH, SOL, BNB, DOGE.",
        ),
        Tool(
            name="calculer_portefeuille",
            func=calculer_valeur_portefeuille,
            description="Calcule la valeur d'un portefeuille d'actions avec données yfinance. "
            "Entrée : SYMBOLE:QUANTITE|SYMBOLE:QUANTITE ex AAPL:10|MSFT:5|LVMH:2. "
            "Retourne valeur par ligne, total et variation globale du jour.",
        ),
        # ── Outil 3 : Calculs financiers ──────────────────────────────────
        Tool(
            name="calculer_tva",
            func=calculer_tva,
            description="Calcule TVA et prix TTC. Entrée : prix_ht,taux ex 100,20.",
        ),
        Tool(
            name="calculer_interets",
            func=calculer_interets_composes,
            description="Intérêts composés. Entrée : capital,taux_annuel,années ex 10000,5,3.",
        ),
        Tool(
            name="calculer_marge",
            func=calculer_marge,
            description="Marge commerciale. Entrée : prix_vente,cout_achat ex 150,80.",
        ),
        Tool(
            name="calculer_mensualite",
            func=calculer_mensualite_pret,
            description="Mensualité prêt. Entrée : capital,taux_annuel,mois ex 200000,3.5,240.",
        ),
        # ── Outil 4 : API publique ────────────────────────────────────────
        Tool(
            name="convertir_devise",
            func=convertir_devise,
            description="Conversion de devises en temps réel (API Frankfurter). "
            "Entrée : montant,DEV_SOURCE,DEV_CIBLE ex 100,USD,EUR.",
        ),
        # ── Outil 5 : Transformation de texte ────────────────────────────
        Tool(
            name="resumer_texte",
            func=resumer_texte,
            description="Résume un texte et donne des statistiques. Entrée : texte complet.",
        ),
        Tool(
            name="formater_rapport",
            func=formater_rapport,
            description="Formate en rapport. Entrée : Cle1:Val1|Cle2:Val2.",
        ),
        Tool(
            name="extraire_mots_cles",
            func=extraire_mots_cles,
            description="Extrait les mots-clés d'un texte. Entrée : texte complet.",
        ),
        # ── Outil 6 : Recommandation ─────────────────────────────────────
        Tool(
            name="recommander_produits",
            func=recommander_produits,
            description="Recommandations produits. "
            "Entrée : budget,categorie,type_compte ex 300,Informatique,Premium. "
            "Catégories : Informatique, Mobilier, Audio, Toutes. "
            "Types : Standard, Premium, VIP.",
        ),
    ]

    # ── Outil 7 : Recherche web Tavily ─────────────────────────────────
    try:
        tools.append(
            TavilySearchResults(
                name="recherche_web",
                description="Recherche des informations web récentes (actualités, entreprises, événements). "
                "Entrée : requête textuelle en français ou en anglais.",
                max_results=5,
                include_raw_content=False,
                include_answer=True,
            )
        )
    except Exception:
        tools.append(
            Tool(
                name="recherche_web",
                func=_recherche_web_indisponible,
                description="Recherche web récente via Tavily. Entrée : requête textuelle.",
            )
        )

    # ── Outil 8 : Python REPL ───────────────────────────────────────────
    python_repl = PythonREPLTool()

    def _python_repl_wrapper(code: str) -> str:
        return _executer_code_python(code, python_repl)

    # ATTENTION SECURITE : cet outil exécute du code arbitraire.
    # Ne jamais utiliser en production sans sandbox.
    tools.append(
        Tool(
            name="python_repl",
            func=_python_repl_wrapper,
            description=(
                "Exécute du code Python pour des calculs complexes ou traitements "
                "de données non couverts par les autres outils. "
                "Entrée : code Python valide sous forme de chaîne."
            ),
        )
    )

    return tools


def creer_agent():
    """Crée et retourne un agent LangChain configuré."""
    tools = creer_tools()

    # Initialisation du LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # Chargement du prompt ReAct depuis le hub LangChain
    # Ce prompt enseigne au LLM le cycle Thought → Action → Observation
    prompt = hub.pull("hwchase17/react")
    # Création de l'agent avec la stratégie ReAct
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

    # Création de l'exécuteur
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,  # Affiche le raisonnement étape par étape
        max_iterations=10,  # Évite les boucles infinies
        handle_parsing_errors=True,
    )

    return agent_executor


def interroger_agent(agent, question: str):
    """Envoie une question à l'agent et affiche la réponse finale."""
    print(f"\n{'=' * 60}")
    print(f"Question : {question}")
    print("=" * 60)
    result = agent.invoke({"input": question})
    print(f"\nRéponse finale : {result['output']}")
    return result
