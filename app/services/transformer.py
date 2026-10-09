import pandas as pd


def transformer_bpaca(df):

    df = df.copy()

    # renommage
    df = df.rename(
        columns={
            "Date de comptabilisation": "Date"
        }
    )

    # insertion Facture en position 3
    df.insert(2, "Facture", False)

    # colonnes supplémentaires
    df["Lien"] = ""
    df["Type TVA"] = ""

    df["HT 20,0%"] = ""
    df["HT 5,5%"] = ""
    df["HT 10,0%"] = ""

    df["TVA 20,0%"] = ""
    df["TVA 5,5%"] = ""
    df["TVA 10,0%"] = ""

    return df