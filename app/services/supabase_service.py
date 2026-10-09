from dotenv import load_dotenv
from supabase import create_client
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

        lignes.append({
            "compte": row["Compte"],
            "date": date_fr_vers_iso(row["Date"]),
            "facture": row["Facture"],
            "date_operation": date_fr_vers_iso(row["Date opération"]),
            "libelle": row["Libellé"],
            "reference": row["Référence"],
            "date_valeur": date_fr_vers_iso(row["Date valeur"]),
            "montant": row["Montant"],
            "lien": row["Lien"],
            "type_tva": row["Type TVA"],
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