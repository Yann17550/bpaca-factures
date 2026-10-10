import streamlit as st

from services.exercise_service import (
    lister_exercices,
    get_exercice_actif,
    set_exercice_actif
)


def afficher_navigation():

    exercices = lister_exercices()

    exercice_actif = get_exercice_actif()

    if not exercice_actif and exercices:

        exercice_actif = exercices[-1]

        set_exercice_actif(
            exercice_actif
        )

    with st.sidebar:

        st.title(
            "📊 BPACA"
        )

        st.divider()

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

            if nouvel_exercice != exercice_actif:

                set_exercice_actif(
                    nouvel_exercice
                )

                st.rerun()

        else:

            nouvel_exercice = None

            st.warning(
                "Aucun exercice trouvé."
            )

        st.divider()

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

    return page, nouvel_exercice