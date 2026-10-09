import pandas as pd


def transformer_bpaca(df):

    df = df.copy()

    # Renommage

    df = df.rename(
        columns={
            "Date de comptabilisation": "Date"
        }
    )

    # Colonne Facture

    df.insert(
        2,
        "Facture",
        False
    )

    # Colonnes métier

    df["Lien"] = ""
    df["Type TVA"] = pd.NA

    df["HT 20,0%"] = 0.0
    df["HT 5,5%"] = 0.0
    df["HT 10,0%"] = 0.0

    df["TVA 20,0%"] = 0.0
    df["TVA 5,5%"] = 0.0
    df["TVA 10,0%"] = 0.0

    # Montant du CSV

    df["Montant"] = (
        df["Montant"]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    # Colonnes monétaires

    colonnes_numeriques = [
        "Montant",
        "HT 20,0%",
        "HT 5,5%",
        "HT 10,0%",
        "TVA 20,0%",
        "TVA 5,5%",
        "TVA 10,0%"
    ]

    for colonne in colonnes_numeriques:

        df[colonne] = (
            pd.to_numeric(
                df[colonne],
                errors="coerce"
            )
            .fillna(0)
        )

    return df