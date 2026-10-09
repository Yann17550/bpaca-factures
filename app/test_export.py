from services.csv_importer import lire_csv_bpaca
from services.transformer import transformer_bpaca
from services.tva_calculator import calculer_tva
from services.excel_exporter import exporter_excel

fichier_csv = r"data/imports/BPACA_OP_20260704.csv"

df = lire_csv_bpaca(fichier_csv)

df = transformer_bpaca(df)

df = calculer_tva(df)

exporter_excel(
    df,
    r"data/exports/test.xlsx"
)

print("Export terminé")