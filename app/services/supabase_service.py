from dotenv import load_dotenv
from supabase import create_client
import pandas as pd
import os

from services.utils import date_fr_vers_iso


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


def insert_operations(df):

    lignes = []

    for _, row in df.iterrows():

        montant = float(row["Montant"])

        debit = abs(montant) if montant < 0 else 0.0
        credit = montant if montant > 0 else 0.0

        type_tva = row["Type TVA"]

        if pd.isna(type_tva) or str(type_tva).strip() == "":
            type_tva = None

        lignes.append({
            "compte": row["Compte"],
            "date": date_fr_vers_iso(row["Date"]),
            "facture": row["Facture"],

            "date_operation": date_fr_vers_iso(
                row["Date opération"]
            ),

            "libelle": row["Libellé"],
            "reference": row["Référence"],

            "date_valeur": date_fr_vers_iso(
                row["Date valeur"]
            ),

            "montant": montant,

            "debit": debit,
            "credit": credit,

            "lien": row["Lien"],
            "type_tva": type_tva,

            "ht_20": row["HT 20,0%"],
            "ht_55": row["HT 5,5%"],
            "ht_10": row["HT 10,0%"],

            "tva_20": row["TVA 20,0%"],
            "tva_55": row["TVA 5,5%"],
            "tva_10": row["TVA 10,0%"]
        })

    resultat = (
        supabase
        .table("operations")
        .insert(lignes)
        .execute()
    )

    return resultat


def get_operations():

    resultat = (
        supabase
        .table("operations")
        .select("*")
        .order("date")
        .execute()
    )

    return resultat.data


def update_operation(
    operation_id,
    facture,
    type_tva,
    lien
):

    if pd.isna(type_tva) or str(type_tva).strip() == "":
        type_tva = None

    resultat = (
        supabase
        .table("operations")
        .update(
            {
                "facture": facture,
                "type_tva": type_tva,
                "lien": lien
            }
        )
        .eq("id", operation_id)
        .execute()
    )

    return resultat

def get_cles_operations():

    resultat = (
        supabase
        .table("operations")
        .select(
            "date_operation,montant,reference"
        )
        .execute()
    )

    cles = set()

    for ligne in resultat.data:

        cle = (
            str(ligne["date_operation"]),
            round(float(ligne["montant"]), 2),
            str(ligne["reference"])
        )

        cles.add(cle)

    return cles