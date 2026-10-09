import pandas as pd


def lire_csv_bpaca(fichier_csv):

    donnees = []

    with open(
        fichier_csv,
        "r",
        encoding="latin1"
    ) as f:

        # saute l'entête
        next(f)

        for ligne in f:

            ligne = ligne.strip()
            ligne = ligne.strip('"')

            morceaux = ligne.split("\t")

            # retire la dernière colonne vide éventuelle
            while morceaux and morceaux[-1] == "":
                morceaux.pop()

            compte = morceaux[0]
            date_compta = morceaux[1]
            date_operation = morceaux[2]

            montant = morceaux[-1]
            date_valeur = morceaux[-2]
            reference = morceaux[-3]

            libelle = " ".join(morceaux[3:-3]).strip()

            donnees.append({
                "Compte": compte,
                "Date de comptabilisation": date_compta,
                "Date opération": date_operation,
                "Libellé": libelle,
                "Référence": reference,
                "Date valeur": date_valeur,
                "Montant": montant
            })

    return pd.DataFrame(donnees)