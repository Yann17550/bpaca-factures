import pandas as pd
import streamlit as st

from services.supabase_service import (
    get_operations,
    update_operation,
    insert_operations,
    get_cles_operations
)
from services.utils import (
    date_fr_vers_iso
)

from services.navigation_service import (
    afficher_navigation
)

from services.bpaca_import_service import (
    lister_fichiers_bpaca,
    get_fichier_bpaca
)

from services.csv_importer import (
    lire_csv_bpaca
)

from services.transformer import (
    transformer_bpaca
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

page, exercice_actif = (
    afficher_navigation()
)

st.subheader(
    "📥 Import BPACA"
)

# --------------------------------------------------
# IMPORT BPACA
# --------------------------------------------------

if page == "Import BPACA":

    if "import_message" in st.session_state:

        st.success(
            st.session_state["import_message"]
        )

        del st.session_state[
            "import_message"
        ]
    
    st.subheader(
        "📥 Import BPACA"
    )

    fichiers = lister_fichiers_bpaca()

    if not fichiers:

        st.warning(
            "Aucun fichier trouvé dans BPACA_OP."
        )

        st.stop()

    fichier_selectionne = st.selectbox(
        "Fichier BPACA à importer",
        fichiers
    )

    chemin_fichier = get_fichier_bpaca(
        fichier_selectionne
    )

    st.caption(
        chemin_fichier
    )

    if st.button(
        "📥 Importer le fichier"
    ):

        try:

            df_import = lire_csv_bpaca(
                chemin_fichier
            )

            df_import = transformer_bpaca(
                df_import
            )

            cles_existantes = get_cles_operations()

            df_import["cle_doublon"] = list(
                zip(
                    df_import["Date opération"]
                        .apply(date_fr_vers_iso),

                    df_import["Montant"]
                        .round(2),

                    df_import["Référence"]
                        .astype(str)
                )
            )

            nb_total = len(df_import)

            df_import = df_import[
                ~df_import["cle_doublon"]
                    .isin(cles_existantes)
            ]

            nb_importees = len(df_import)

            nb_doublons = (
                nb_total
                - nb_importees
            )

            df_import = df_import.drop(
                columns=["cle_doublon"]
            )

            if nb_importees > 0:

                insert_operations(
                    df_import
                )

            st.session_state["import_message"] = (
                f"{nb_importees} opération(s) importée(s) | "
                f"{nb_doublons} doublon(s) ignoré(s)"
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Erreur : {e}"
            )

    st.stop()

# --------------------------------------------------
# FUTURES PAGES
# --------------------------------------------------

if page != "Opérations":

    st.warning(
        "🚧 Fonctionnalité en cours de développement"
    )

    st.stop()

# --------------------------------------------------
# DONNÉES
# --------------------------------------------------

operations = get_operations()

df = pd.DataFrame(
    operations
)

if df.empty:

    st.info(
        "Aucune opération dans la base."
    )

    st.stop()

df = df[
    ~df["libelle"].str.contains(
        "COM CB|REMISE CB",
        case=False,
        na=False
    )
]

# --------------------------------------------------
# INFORMATIONS TVA
# --------------------------------------------------

st.info(
    """
Pour remplir le champ Type TVA :

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

# --------------------------------------------------
# VALIDATION TVA
# --------------------------------------------------

tableau["etat_tva"] = (
    tableau["type_tva"]
    .apply(get_tva_state)
)

nb_non_traites = (
    tableau["etat_tva"]
    == "⏳ À traiter"
).sum()

nb_erreurs = (
    tableau["etat_tva"]
    == "🚨 ERREUR"
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

# --------------------------------------------------
# SAUVEGARDE
# --------------------------------------------------

if st.button(
    "💾 Enregistrer les modifications"
):

    erreurs = []

    for _, row in tableau.iterrows():

        valeur = row["type_tva"]

        if pd.isna(valeur):

            valeur = None

        else:

            valeur = str(
                valeur
            ).strip()

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