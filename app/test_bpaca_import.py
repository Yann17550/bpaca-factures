from services.bpaca_import_service import (
    get_dossier_bpaca,
    lister_fichiers_bpaca
)

print(
    "Dossier BPACA :"
)

print(
    get_dossier_bpaca()
)

print(
    "\nFichiers disponibles :"
)

for fichier in lister_fichiers_bpaca():

    print(fichier)