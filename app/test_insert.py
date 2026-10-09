from services.csv_importer import lire_csv_bpaca
from services.transformer import transformer_bpaca
from services.supabase_service import insert_operations


fichier_csv = r"data/imports/BPACA_OP_20260704.csv"

df = lire_csv_bpaca(fichier_csv)

df = transformer_bpaca(df)

resultat = insert_operations(df)

print("Insertion terminée")

print(
    f"{len(resultat.data)} lignes envoyées"
)