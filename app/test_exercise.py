from services.exercise_service import get_racine

print("\nRacine :")
print(get_racine())




from services.exercise_service import (
    exercice_suggere,
    lister_exercices,
    exercice_existe,
    nom_nouvel_exercice,
    structure_exercice
)

print("Exercice suggéré :")
print(exercice_suggere())

print("\nExercices existants :")
print(lister_exercices())

print("\n2026-2027 existe ?")
print(
    exercice_existe(
        "2026-2027"
    )
)

print("\nNom prochain exercice :")
print(
    nom_nouvel_exercice(
        "2027-2028"
    )
)

print("\nStructure :")
for dossier in structure_exercice():
    print(dossier)