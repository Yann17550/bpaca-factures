import streamlit as st

from views.import_bpaca_view import (
    afficher_import_bpaca
)
from views.operations_view import (
    afficher_operations
)

from services.navigation_service import (
    afficher_navigation
)

from services.bpaca_import_service import (
    lister_fichiers_bpaca,
    get_fichier_bpaca
)


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

    afficher_import_bpaca()

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
# OPÉRATIONS
# --------------------------------------------------


if page == "Opérations":


    afficher_operations()


    st.stop()