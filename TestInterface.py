import streamlit as st
import pandas as pd
import numpy as np

# Configuration de la page
st.set_page_config(page_title="Budget Citoyen - Simulateur de Précision", layout="wide")

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stAlert { border-left: 5px solid #007bff; }
    .status-box { padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE DU MOTEUR CAUSAL (COEFFICIENTS RÉELS) ---
# Constantes basées sur les données officielles [cite: 1, 44, 109]
COEFF_TVA = 11.0          # 1% = 11 Md€
COEFF_IS = 2.5            # 1% = 2.5 Md€
COEFF_CSG = 14.0          # 1% = 14 Md€
COEFF_INDICE = 2.3        # 1% = 2.3 Md€
PIVOT_DGF = 27.2          # Valeur pivot en Md€

# --- HEADER ---
st.title("🏛️ Simulateur Budget Citoyen")
st.markdown("""
**Prenez les commandes des finances publiques.** Ce simulateur utilise une **rigueur statique n-1** : il calcule l'impact comptable immédiat des mesures sans spéculation sur la croissance[cite: 36, 105].
""")

# --- BARRE LATÉRALE : LEVIERS ET POP-OVERS ---
st.sidebar.header("🎛️ Leviers de Commande")

# Section ÉTAT
st.sidebar.subheader("1. État Central")

# Levier TVA
val_tva = st.sidebar.slider("Taux normal TVA (%)", 15.0, 25.0, 20.0, step=0.1)
diff_tva = (val_tva - 20.0) * COEFF_TVA

with st.sidebar.popover("❓ Enjeux : TVA"):
    st.markdown("**Qu'est-ce que c'est ?**")
    st.write("Taxe sur la consommation, première recette de l'État.")
    st.divider()
    st.markdown("**🔍 Bloc Institutionnel (Faits)**")
    st.write("Impôt au rendement élevé, stable, mais proportionnel : il pèse plus lourd dans le budget des ménages modestes (consommant tout leur revenu).")
    st.markdown("**⚖️ Bloc Idéologique (Débats)**")
    st.markdown("- *Pro-hausse :* Moyen rapide de réduire le déficit sans décourager l'investissement[cite: 100].")
    st.markdown("- *Anti-hausse :* Injuste socialement, frappe de plein fouet le pouvoir d'achat des bas revenus[cite: 101].")
    st.link_button("🔗 Source : Commission des Finances", "https://www.assemblee-nationale.fr")

# Levier IS
val_is = st.sidebar.slider("Taux Impôt Sociétés (%)", 15.0, 35.0, 25.0, step=0.5)
diff_is = (val_is - 25.0) * COEFF_IS

# Section SÉCURITÉ SOCIALE
st.sidebar.subheader("2. Protection Sociale")
val_csg = st.sidebar.slider("Taux CSG Activité (%)", 7.0, 12.0, 9.2, step=0.1)
diff_csg = (val_csg - 9.2) * COEFF_CSG

# Section FONCTIONNAIRES & TERRITOIRES
st.sidebar.subheader("3. Dépenses & Territoires")
val_indice = st.sidebar.slider("Point d'indice (%)", -2.0, 5.0, 0.0, step=0.5)
diff_indice = -(val_indice * COEFF_INDICE) # Hausse indice = hausse dépense = impact négatif solde

val_dgf = st.sidebar.slider("Dotation DGF (Md€)", 20.0, 35.0, PIVOT_DGF, step=0.1)
diff_dgf = -(val_dgf - PIVOT_DGF)

# --- CALCUL DU SOLDE GLOBAL ---
impact_total = diff_tva + diff_is + diff_csg + diff_indice + diff_dgf

# --- AFFICHAGE DES RÉSULTATS (LES TROIS CYLINDRES) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Solde État (AC)", "-145 Md€", f"{diff_tva + diff_is + diff_dgf:.1f} Md€")
    st.caption("Flux : TVA, IS, DGF, Éducation [cite: 45]")

with col2:
    st.metric("Solde Sécu (ASSO)", "-8.0 Md€", f"{diff_csg:.1f} Md€")
    st.caption("Flux : CSG, Cotisations, ONDAM [cite: 48]")

with col3:
    st.metric("Solde Local (APUL)", "+2.0 Md€", f"{-diff_dgf:.1f} Md€")
    st.caption("Flux : DGF, Fiscalité locale [cite: 50]")

# --- BOUTON PREUVE ---
st.info(f"**🔬 Preuve de Calcul :** Impact Total = {impact_total:.1f} Md€.  \n*Formule : Recette Finale = (Assiette n-1) * (Nouveau Taux)*.")

st.divider()

# --- GRAPHIQUE DE DISTRIBUTION DYNAMIQUE ---
st.subheader("📊 Impact social : Distribution par Déciles de Revenus")
st.markdown("*Ce graphique montre la perte ou le gain de pouvoir d'achat selon le niveau de revenu (D1 = 10% les plus pauvres).*")

# Simulation visuelle de l'impact TVA (plus fort sur D1-D3)
# On crée un multiplicateur de régression
base_impact = (val_tva - 20.0) * 0.5
multiplicateurs = np.array([2.5, 2.0, 1.5, 1.2, 1.0, 0.8, 0.7, 0.6, 0.5, 0.4])
impact_deciles = - (base_impact * multiplicateurs)

data_distribution = pd.DataFrame({
    'Déciles': ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10'],
    'Variation Pouvoir Achat (%)': impact_deciles
})

st.bar_chart(data_distribution, x='Déciles', y='Variation Pouvoir Achat (%)', color='#ff4b4b' if base_impact > 0 else '#28a745')

st.caption("Visualisation liée au Levier TVA : Observez comme les barres D1 à D3 sont plus sensibles aux variations du taux.")

# --- FOOTER PÉDAGOGIQUE ---
st.markdown("---")
st.caption("Projet Budget Citoyen | Expertise Data & Finances Publiques | Architecture Multi-Axes [cite: 121]")