import pandas as pd
import streamlit as st

from services.supabase_service import (
    get_operations,
    update_operation
)


TVA_VALIDES = {
    None,
    "",
    "0",
    "1",
    "2",
    "5",
    "s"
}


def get_tva_state(valeur):

    if pd.isna(valeur):
        return "⏳ À traiter"

    valeur = str(valeur).strip()

    if valeur == "":
        return "⏳ À traiter"

    if valeur in {"0", "1", "2", "5"}:
        return "✅ OK"

    if valeur == "s":
        return "🟧 Multi TVA"

    return "🚨 ERREUR"


st.set_page_config(
    page_title="BPACA Factures",
    layout="wide"
)

st.title("📊 BPACA Factures")

operations = get_operations()

df = pd.DataFrame(operations)

df = df[
    ~df["libelle"].str.contains(
        "COM CB|REMISE CB",
        case=False,
        na=False
    )
]

st.info(
    """
Pour remplir le champType TVA :

• vide = non traité

• 0 = sans TVA

• 5 = TVA 5,5 %

• 1 = TVA 10 %

• 2 = TVA 20 %

• s = multi TVA
"""
)

colonnes_editables = [
    "id",
    "facture",
    "type_tva",
    "lien"
]

tableau = st.data_editor(
    df,
    use_container_width=True,
    hide_index=True,
    disabled=[
        col
        for col in df.columns
        if col not in colonnes_editables
    ],
    column_config={
        "montant": st.column_config.NumberColumn(
            "Montant",
            format="%.2f"
        ),

        "debit": st.column_config.NumberColumn(
            "Débit",
            format="%.2f"
        ),

        "credit": st.column_config.NumberColumn(
            "Crédit",
            format="%.2f"
        ),

        "ht_20": st.column_config.NumberColumn(
            "HT 20 %",
            format="%.2f"
        ),

        "ht_55": st.column_config.NumberColumn(
            "HT 5,5 %",
            format="%.2f"
        ),

        "ht_10": st.column_config.NumberColumn(
            "HT 10 %",
            format="%.2f"
        ),

        "tva_20": st.column_config.NumberColumn(
            "TVA 20 %",
            format="%.2f"
        ),

        "tva_55": st.column_config.NumberColumn(
            "TVA 5,5 %",
            format="%.2f"
        ),

        "tva_10": st.column_config.NumberColumn(
            "TVA 10 %",
            format="%.2f"
        ),
    }
)

# -------------------------
# VALIDATION IMMEDIATE
# -------------------------

tableau["etat_tva"] = (
    tableau["type_tva"]
    .apply(get_tva_state)
)

nb_non_traites = (
    tableau["etat_tva"] == "⏳ À traiter"
).sum()

nb_erreurs = (
    tableau["etat_tva"] == "🚨 ERREUR"
).sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Nombre d'opérations",
        len(tableau)
    )

with col2:
    st.metric(
        "À traiter",
        nb_non_traites
    )

with col3:
    st.metric(
        "Erreurs TVA",
        nb_erreurs
    )

if nb_erreurs > 0:

    st.error(
        f"🚨 {nb_erreurs} erreur(s) TVA détectée(s)"
    )

# -------------------------
# SAUVEGARDE
# -------------------------

if st.button("💾 Enregistrer les modifications"):

    erreurs = []

    for _, row in tableau.iterrows():

        valeur = row["type_tva"]

        if pd.isna(valeur):
            valeur = None
        else:
            valeur = str(valeur).strip()

        if valeur not in TVA_VALIDES:

            erreurs.append(
                f"ID {row['id']} → {valeur}"
            )

    if erreurs:

        st.error(
            "Enregistrement refusé : TVA invalide."
        )

        for erreur in erreurs:
            st.write(erreur)

        st.stop()

    for _, row in tableau.iterrows():

        update_operation(
            row["id"],
            row["facture"],
            row["type_tva"],
            row["lien"]
        )

    st.success(
        "Modifications enregistrées"
    )

    st.rerun()