from langchain_classic.tools import Tool
from tools.database import rechercher_produit, rechercher_client
from tools.finance import obtenir_cours_action, obtenir_cours_crypto
from tools.calculations import calculer_tva, calculer_marge, calculer_interets_composes, calculer_mensualite_pret
from tools.public_api import convertir_devise
from tools.recommendation import recommander_produits
from tools.text import resumer_texte, formater_rapport, extraire_mots_cles

# ── Outil 1 : Base de données ─────────────────────────────────────
Tool(name='rechercher_client',
     func=rechercher_client,
     description='Recherche un client par nom ou ID (ex: C001). ' 'Retourne solde, type de compte, historique achats.'),

Tool(name='rechercher_produit',
     func=rechercher_produit,
     description='Recherche un produit par nom ou ID. ' 'Retourne prix HT, TVA, prix TTC, stock.'),

 # ── Outil 2 : Données financières ─────────────────────────────────
Tool(name='cours_action', func=obtenir_cours_action,
         description='Cours boursier d\'une action. '
                     'Entrée : symbole majuscule ex AAPL, MSFT, TSLA, LVMH, AIR.'),
 
Tool(name='cours_crypto', func=obtenir_cours_crypto,
         description='Cours d\'une crypto. '
                     'Entrée : symbole ex BTC, ETH, SOL, BNB, DOGE.'),

# ── Outil 3 : Calculs financiers ──────────────────────────────────
Tool(name='calculer_tva', func=calculer_tva,
         description='Calcule TVA et prix TTC. Entrée : prix_ht,taux ex 100,20.'),
 
Tool(name='calculer_interets', func=calculer_interets_composes,
         description='Intérêts composés. Entrée : capital,taux_annuel,années ex 10000,5,3.'),
 
Tool(name='calculer_marge', func=calculer_marge,
         description='Marge commerciale. Entrée : prix_vente,cout_achat ex 150,80.'),
 
Tool(name='calculer_mensualite', func=calculer_mensualite_pret,
         description='Mensualité prêt. Entrée : capital,taux_annuel,mois ex 200000,3.5,240.'),

# ── Outil 4 : API publique ────────────────────────────────────────
Tool(name='convertir_devise', func=convertir_devise,
         description='Conversion de devises en temps réel (API Frankfurter). '
                     'Entrée : montant,DEV_SOURCE,DEV_CIBLE ex 100,USD,EUR.'),


# ── Outil 5 : Transformation de texte ────────────────────────────
Tool(name='resumer_texte', func=resumer_texte,
         description='Résume un texte et donne des statistiques. Entrée : texte complet.'),
 
Tool(name='formater_rapport', func=formater_rapport,
         description='Formate en rapport. Entrée : Cle1:Val1|Cle2:Val2.'),
 
Tool(name='extraire_mots_cles', func=extraire_mots_cles,
         description='Extrait les mots-clés d\'un texte. Entrée : texte complet.'),

# ── Outil 6 : Recommandation ─────────────────────────────────────
Tool(name='recommander_produits', func=recommander_produits,
     description='Recommandations produits. '
                 'Entrée : budget,categorie,type_compte ex 300,Informatique,Premium. '
                 'Catégories : Informatique, Mobilier, Audio, Toutes. '
                 'Types : Standard, Premium, VIP.'),

