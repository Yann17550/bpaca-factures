from services.csv_importer import lire_csv_bpaca
from services.transformer import transformer_bpaca

FICHIER = r"data/imports/BPACA_OP_20260704.csv"

df = lire_csv_bpaca(FICHIER)

df = transformer_bpaca(df)

print()
print(df.columns.tolist())

print()
print(df.head())