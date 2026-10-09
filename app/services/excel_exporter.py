from openpyxl import Workbook
from openpyxl.worksheet.table import Table
from openpyxl.worksheet.table import TableStyleInfo
from openpyxl.styles import Font
from openpyxl.styles import Alignment
from openpyxl.styles import PatternFill
from openpyxl.formatting.rule import FormulaRule

def exporter_excel(df, fichier_sortie):

    wb = Workbook()

    ws = wb.active
    ws.title = "Factures"

    # Entêtes
    for col, nom_colonne in enumerate(df.columns, start=1):
        ws.cell(
            row=1,
            column=col,
            value=nom_colonne
        )

    # Données
    for ligne, row in enumerate(
        df.itertuples(index=False),
        start=2
    ):
        for col, valeur in enumerate(row, start=1):
            ws.cell(
                row=ligne,
                column=col,
                value=valeur
            )

    # Création du tableau Excel
    derniere_ligne = ws.max_row
    derniere_colonne = ws.max_column

    lettre_fin = ws.cell(
        1,
        derniere_colonne
    ).column_letter

    table = Table(
        displayName="Tableau1",
        ref=f"A1:{lettre_fin}{derniere_ligne}"
    )

    style = TableStyleInfo(
        name="TableStyleLight8",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False
    )

    table.tableStyleInfo = style

    ws.add_table(table)

    # Entête

    for cell in ws[1]:

        cell.font = Font(
            bold=True,
            size=12,
            color="FFFFFF"
        )

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

    # Hauteur ligne 1

    ws.row_dimensions[1].height = 25.5

    for colonne in ws.columns:

        largeur = 0

        for cell in colonne:

            if cell.value is not None:

                largeur = max(
                    largeur,
                    len(str(cell.value))
                )

        ws.column_dimensions[
            colonne[0].column_letter
        ].width = largeur + 2    

# Colonnes masquées

    ws.column_dimensions["D"].hidden = True
    ws.column_dimensions["F"].hidden = True
    ws.column_dimensions["G"].hidden = True

    # Couleur verte claire

    remplissage = PatternFill(
        fill_type="solid",
        start_color="C6EFCE",
        end_color="C6EFCE"
    )

    # Mise en forme conditionnelle
    # C = colonne Facture

    ws.conditional_formatting.add(
        f"A2:P{ws.max_row}",
        FormulaRule(
            formula=['$C2=TRUE'],
            fill=remplissage
        )
    )
  


    wb.save(fichier_sortie)