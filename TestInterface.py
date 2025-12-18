import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Budget Citoyen - Cockpit de Simulation", layout="wide")

# --- STYLE CSS POUR L'IDENTITÉ VISUELLE ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stAlert { border-left: 5px solid #ff4b4b; }
    .stButton button { width: 100%; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER & PHILOSOPHIE ---
st.title("🏛️ Budget Citoyen : Le Cockpit")
st.subheader("Prenez les commandes des finances publiques (Base exécution n-1)")

with st.expander("ℹ️ À propos de la rigueur scientifique de cet outil", expanded=False):
    st.warning("**Alerte de Statique Récurrente :** Cette simulation est strictement statique. Elle ne prédit pas les changements de comportement ou les effets sur la croissance (ex: une hausse de TVA n'entraîne pas ici de baisse de consommation). L'objectif est la transparence comptable brute.")

# --- BARRE LATÉRALE : LES 12 LEVIERS MACRO ---
st.sidebar.header("🎛️ Leviers de Commande")

def info_popover(label, definition, institutionnel, ideologique, source_url):
    """Génère un composant d'aide pédagogique pour chaque levier."""
    with st.sidebar.popover(f"❓ Enjeux : {label}"):
        st.markdown(f"**Qu'est-ce que c'est ?**\n{definition}")
        st.divider()
        st.markdown(f"**🔍 Bloc Institutionnel (Faits)**\n{institutionnel}")
        st.markdown(f"**⚖️ Bloc Idéologique (Débats)**\n{ideologique}")
        st.link_button("🔗 Voir la source Open Data", source_url)
        st.caption("Formule : Recette = Assiette(n-1) x Nouveau Taux")

# --- SECTION 1 : ÉTAT (AC) ---
st.sidebar.subheader("1. État Central")
tva = st.sidebar.slider("Taux normal TVA (%)", 15.0, 25.0, 20.0, help="Taux pivot de la consommation")
info_popover("TVA", 
             "Premier impôt de France par son rendement.",
             "Impact régressif : pèse proportionnellement plus sur les ménages modestes (D1-D3).",
             "Soutien : Recette stable et difficile à frauder. Opposition : Pénalise le pouvoir d'achat.",
             "https://data.economie.gouv.fr")

irpp = st.sidebar.select_slider("Progressivité IRPP", options=["Allégée", "Actuelle", "Renforcée"], value="Actuelle")
is_taux = st.sidebar.number_input("Taux Impôt Sociétés (%)", 10, 50, 25)

# --- SECTION 2 : SÉCURITÉ SOCIALE (ASSO) ---
st.sidebar.subheader("2. Protection Sociale")
ondam = st.sidebar.slider("Objectif ONDAM (Mds €)", 200, 300, 254)
pensions = st.sidebar.select_slider("Indexation Retraites", options=["Sous-inflation", "Inflation", "Supra-inflation"], value="Inflation")
csg = st.sidebar.slider("Taux CSG Activité (%)", 5.0, 15.0, 9.2)

# --- SECTION 3 : COLLECTIVITÉS (APUL) ---
st.sidebar.subheader("3. Territoires")
dgf = st.sidebar.slider("Dotation Globale (DGF)", 20, 40, 27)

# --- ESPACE DE VISUALISATION (LES TROIS CYLINDRES) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.header("🏢 État")
    st.metric("Solde État", "-145 Md€", f"{ (tva-20)*5 } Md€ (Variation)")
    st.progress(0.4, text="Dépenses régaliennes")

with col2:
    st.header("🏥 Sécu")
    st.metric("Solde ASSO", "-8 Md€", "0 Md€")
    st.progress(0.7, text="Branche Maladie & Vieillesse")

with col3:
    st.header("🏘️ Territoires")
    st.metric("Solde APUL", "+2 Md€", f"{ (dgf-27) } Md€")
    st.progress(0.2, text="Investissement local")

st.divider()

# --- REPRODUCTION DE LA PREUVE & DISTRIBUTION ---
st.subheader("📊 Analyse d'impact sur la population")
tab1, tab2 = st.tabs(["Distribution par Déciles (Revenus)", "Répartition par Secteurs (NAF)"])

with tab1:
    st.info("Visualisation de l'effort fiscal par tranche de revenu (D1 à D10).")
    chart_data = pd.DataFrame({
        'Déciles': ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10'],
        'Impact (en % du revenu)': [1.2, 1.1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
    })
    st.bar_chart(chart_data, x='Déciles', y='Impact (en % du revenu)')
    st.caption("Note : La priorité est donnée à la densité de population plutôt qu'aux moyennes.")

with tab2:
    st.write("Impact sectoriel des mesures sur l'IS et les cotisations.")
    st.table(pd.DataFrame({
        'Secteur (NAF)': ['Industrie', 'Commerce', 'Services'],
        'Variation Charge': ['+2.1%', '-0.5%', '+1.2%']
    }))

# --- FOOTER ---
st.sidebar.divider()
if st.sidebar.button("💾 Générer mon Rapport d'Impact"):
    st.toast("Synthèse en cours de génération...")