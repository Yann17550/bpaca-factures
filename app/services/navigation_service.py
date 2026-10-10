import streamlit as st

from services.exercise_service import (
    lister_exercices,
    get_exercice_actif,
    set_exercice_actif
)


def afficher_navigation():

    if "menu_ouvert" not in st.session_state:

        st.session_state.menu_ouvert = False

    col_menu, col_vide = st.columns([1, 20])

    with col_menu:

        if st.button(
            "☰ Menu",
            use_container_width=True
        ):

            st.session_state.menu_ouvert = (
                not st.session_state.menu_ouvert
            )

    exercice_actif = get_exercice_actif()

    exercices = lister_exercices()

    if not exercice_actif and exercices:

        exercice_actif = exercices[-1]

        set_exercice_actif(
            exercice_actif
        )

    page = "Opérations"

    if st.session_state.menu_ouvert:

        with st.container():

            st.markdown("---")

            if exercices:

                nouvel_exercice = st.selectbox(
                    "Exercice",
                    exercices,
                    index=(
                        exercices.index(
                            exercice_actif
                        )
                        if exercice_actif in exercices
                        else len(exercices) - 1
                    )
                )

                if (
                    nouvel_exercice
                    != exercice_actif
                ):

                    set_exercice_actif(
                        nouvel_exercice
                    )

                    st.rerun()

            st.markdown("---")

            page = st.radio(
                "Navigation",
                [
                    "Opérations",
                    "Import BPACA",
                    "Fournisseurs",
                    "Factures",
                    "Paramètres"
                ]
            )

    return page, exercice_actif