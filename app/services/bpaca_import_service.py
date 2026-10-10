from pathlib import Path

from services.exercise_service import (
    get_exercice_actif,
    dossier_exercice
)


def get_dossier_bpaca():

    exercice = get_exercice_actif()

    if not exercice:

        return None

    dossier = dossier_exercice(
        exercice
    )

    if dossier is None:

        return None

    return dossier / "BPACA_OP"


def lister_fichiers_bpaca():

    dossier = get_dossier_bpaca()

    if dossier is None:

        return []

    if not dossier.exists():

        return []

    fichiers = sorted(
        dossier.glob("*.csv"),
        reverse=True
    )

    return [
        fichier.name
        for fichier in fichiers
    ]


def get_fichier_bpaca(nom_fichier):

    dossier = get_dossier_bpaca()

    if dossier is None:

        return None

    fichier = dossier / nom_fichier

    if not fichier.exists():

        return None

    return str(fichier)