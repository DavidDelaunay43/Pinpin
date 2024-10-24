from PySide2.QtWidgets import QGridLayout

class GridLayout(QGridLayout):
    def first_empty_row(self):
        rows = self.rowCount()  # Nombre de lignes dans le layout
        columns = self.columnCount()  # Nombre de colonnes dans le layout

        for row in range(rows):
            is_empty = True
            for col in range(columns):
                item = self.itemAtPosition(row, col)
                if item is not None:  # Si une cellule de la ligne est occupée
                    is_empty = False
                    break  # La ligne n'est pas vide, on arrête la vérification

            if is_empty:
                return row  # Retourne l'index de la première ligne vide

        # Si aucune ligne vide n'est trouvée, retourne la prochaine ligne disponible
        return rows
