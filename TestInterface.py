import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(page_title="Budget Citoyen - Simulateur Consolidé", layout="wide")

# --- PARAMÈTRES DE RÉFÉRENCE N-1 ---
PIB_FRANCE = 2800  # Md€ approx.
DETTE_INITIALE = 3100 # Md€ approx.
SOLDE_INITIAL_MDE = -154 # Md€
SOLDE_INITIAL_PIB = -5.5 # %

# --- LOGIQUE DE CALCUL (MOTEUR CAUSAL) ---
def calculer_impact(tva, is_taux, csg, ondam, dgf, point_indice):
    # Recettes
    var_recettes = (tva - 20) * 11 + (is_taux - 25) * 2.5 + (csg - 9.2) * 14
    # Dépenses
    var_depenses = (ondam - 254) + (dgf - 27.2) + (point_indice * 2.3)
    
    nouveau_solde_mde = SOLDE_INITIAL_MDE + var_recettes - var_depenses
    nouveau_solde_pib = (nouveau_solde_mde / PIB_FRANCE) * 100
    nouvelle_dette = DETTE_INITIALE - nouveau_solde_mde # Le déficit creuse la dette
    
    return nouveau_solde_mde, nouveau_solde_pib, nouvelle_dette, var_recettes, var_depenses

# --- BARRE LATÉRALE (LEVIERS) ---
st.sidebar.header("🎛️ Leviers Macro (Étage 1)")

# État
with st.sidebar.expander("🏛️ État Central", expanded=True):
    tva = st.slider("TVA (%)", 15.0, 25.0, 20.0, step=0.5)
    is_taux = st.slider("Impôt Sociétés (%)", 15.0, 35.0, 25.0, step=1.0)
    dgf = st.slider("Dotation Collectivités (Md€)", 20.0, 35.0, 27.2, step=0.1)
    point_indice = st.slider("Hausse Point d'indice (%)", 0.0, 5.0, 0.0, step=0.1)

# Sécurité Sociale
with st.sidebar.expander("🏥 Protection Sociale", expanded=True):
    csg = st.slider("CSG Activité (%)", 7.0, 12.0, 9.2, step=0.1)
    ondam = st.number_input("ONDAM (Mds €)", value=254, step=1)

# --- CALCULS EN TEMPS RÉEL ---
solde_mde, solde_pib, dette_totale, v_rec, v_dep = calculer_impact(tva, is_taux, csg, ondam, dgf, point_indice)

# --- HEADER DYNAMIQUE ---
st.title("🏛️ Tableau de Bord des Finances Publiques")
c1, c2, c3 = st.columns(3)
c1.metric("Solde Public (% PIB)", f"{solde_pib:.1f}%", f"{solde_pib - SOLDE_INITIAL_PIB:.2f}%")
c2.metric("Solde Public (Md€)", f"{solde_mde:.1f} Md€", f"{v_rec - v_dep:.1f} Md€")
c3.metric("Dette Publique (Est. Md€)", f"{dette_totale:.0f} Md€")

st.divider()

# --- VISUALISATION CONSOLIDÉE (LES 3 CYLINDRES) ---
st.subheader("📊 Équilibre Consolidé des Administrations (AC + ASSO + APUL)")

# Création du graphique Radial/Gauge pour le déficit
fig = go.Figure(go.Indicator(
    mode = "gauge+number+delta",
    value = solde_mde,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Déficit Global (Milliards d'Euros)"},
    delta = {'reference': SOLDE_INITIAL_MDE},
    gauge = {
        'axis': {'range': [-300, 0]},
        'bar': {'color': "#1f77b4"},
        'steps': [
            {'range': [-300, -154], 'color': "#ffcccc"},
            {'range': [-154, 0], 'color': "#ccffcc"}],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': -154}}))

st.plotly_chart(fig, use_container_width=True)