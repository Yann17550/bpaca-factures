import streamlit as st

from services.supabase_service import (
    insert_operations,
    get_cles_operations
)

from services.utils import (
    date_fr_vers_iso
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


def afficher_import_bpaca():

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

        return

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

            cles_existantes = (
                get_cles_operations()
            )

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