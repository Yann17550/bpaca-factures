import pandas as pd


def calculer_tva(df):

    df = df.copy()

    for index, row in df.iterrows():

        type_tva = str(row["Type TVA"]).strip().lower()

        montant = abs(float(row["Montant"]))

        # Remise à zéro des colonnes TVA

        df.at[index, "HT 20,0%"] = 0.0
        df.at[index, "HT 5,5%"] = 0.0
        df.at[index, "HT 10,0%"] = 0.0

        df.at[index, "TVA 20,0%"] = 0.0
        df.at[index, "TVA 5,5%"] = 0.0
        df.at[index, "TVA 10,0%"] = 0.0

        # Sans TVA

        if type_tva == "0":
            continue

        # Multi TVA

        if type_tva == "s":
            continue

        # TVA 5,5 %

        if type_tva == "5":

            ht = round(montant / 1.055, 2)
            tva = round(montant - ht, 2)

            df.at[index, "HT 5,5%"] = ht
            df.at[index, "TVA 5,5%"] = tva

        # TVA 10 %

        elif type_tva == "1":

            ht = round(montant / 1.10, 2)
            tva = round(montant - ht, 2)

            df.at[index, "HT 10,0%"] = ht
            df.at[index, "TVA 10,0%"] = tva

        # TVA 20 %

        elif type_tva == "2":

            ht = round(montant / 1.20, 2)
            tva = round(montant - ht, 2)

            df.at[index, "HT 20,0%"] = ht
            df.at[index, "TVA 20,0%"] = tva

    return df