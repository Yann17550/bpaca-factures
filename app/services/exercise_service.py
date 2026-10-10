import json
import re
from datetime import datetime
from pathlib import Path


CONFIG_FILE = Path("app/config.json")


MOIS_EXERCICE = [
    "M01 - Octobre",
    "M02 - Novembre",
    "M03 - Décembre",
    "M04 - Janvier",
    "M05 - Février",
    "M06 - Mars",
    "M07 - Avril",
    "M08 - Mai",
    "M09 - Juin",
    "M10 - Juillet",
    "M11 - Août",
    "M12 - Septembre"
]


SOUS_DOSSIERS_FIXES = [
    "BPACA_OP",
    "Caisse Yann Pellé",
    "Extraits de compte"
]


def charger_config():

    if not CONFIG_FILE.exists():

        return {
            "racine": ""
        }

    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def sauvegarder_config(config):

    with open(
        CONFIG_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            config,
            f,
            indent=4,
            ensure_ascii=False
        )


def get_racine():

    config = charger_config()

    return config.get(
        "racine",
        ""
    )


def set_racine(chemin):

    config = charger_config()

    config["racine"] = chemin

    sauvegarder_config(config)


def exercice_suggere():

    aujourd_hui = datetime.today()

    annee = aujourd_hui.year
    mois = aujourd_hui.month

    if mois >= 10:

        debut = annee
        fin = annee + 1

    else:

        debut = annee - 1
        fin = annee

    return f"{debut}-{fin}"


def lister_exercices():

    racine = Path(get_racine())

    if not racine.exists():

        return []

    exercices = []

    pattern = re.compile(
        r"Factures Exercice (\d{4}-\d{4})"
    )

    for dossier in racine.iterdir():

        if not dossier.is_dir():
            continue

        m = pattern.search(
            dossier.name
        )

        if m:

            exercices.append(
                m.group(1)
            )

    exercices.sort()

    return exercices


def dossier_exercice(exercice):

    racine = Path(get_racine())

    if not racine.exists():

        return None

    for dossier in racine.iterdir():

        if (
            dossier.is_dir()
            and exercice in dossier.name
        ):

            return dossier

    return None


def exercice_existe(exercice):

    return dossier_exercice(
        exercice
    ) is not None


def prochain_numero_exercice():

    racine = Path(get_racine())

    maximum = 0

    if not racine.exists():

        return 1

    for dossier in racine.iterdir():

        if not dossier.is_dir():
            continue

        m = re.match(
            r"(\d+)",
            dossier.name
        )

        if m:

            maximum = max(
                maximum,
                int(m.group(1))
            )

    return maximum + 1


def nom_nouvel_exercice(exercice):

    numero = prochain_numero_exercice()

    return (
        f"{numero:02d} - "
        f"Factures Exercice {exercice}"
    )


def creer_exercice(exercice):

    racine = Path(
        get_racine()
    )

    nom = nom_nouvel_exercice(
        exercice
    )

    dossier_principal = (
        racine / nom
    )

    dossier_principal.mkdir(
        parents=True,
        exist_ok=True
    )

    for dossier in SOUS_DOSSIERS_FIXES:

        (
            dossier_principal
            / dossier
        ).mkdir(
            exist_ok=True
        )

    for dossier in MOIS_EXERCICE:

        (
            dossier_principal
            / dossier
        ).mkdir(
            exist_ok=True
        )

    return str(
        dossier_principal
    )


def structure_exercice():

    return (
        SOUS_DOSSIERS_FIXES
        + MOIS_EXERCICE
    )

def get_exercice_actif():

    config = charger_config()

    return config.get(
        "exercice_actif",
        None
    )


def set_exercice_actif(exercice):

    config = charger_config()

    config["exercice_actif"] = exercice

    sauvegarder_config(config)