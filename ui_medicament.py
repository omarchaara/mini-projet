from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox
from models import db


class MedicamentUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Médicaments")
        self.setGeometry(100, 100, 700, 500)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Champs de saisie
        self.nom_input = QLineEdit(self)
        self.nom_input.setPlaceholderText("Nom du Médicament")
        self.prix_input = QLineEdit(self)
        self.prix_input.setPlaceholderText("Prix")
        self.dosage_input = QLineEdit(self)
        self.dosage_input.setPlaceholderText("Dosage")
        self.date_fabrication_input = QLineEdit(self)
        self.date_fabrication_input.setPlaceholderText("Date de Fabrication")
        self.fournisseur_select = QComboBox(self)

        # Charger les fournisseurs dans le menu déroulant
        self.load_fournisseurs()

        layout.addWidget(self.nom_input)
        layout.addWidget(self.prix_input)
        layout.addWidget(self.dosage_input)
        layout.addWidget(self.date_fabrication_input)
        layout.addWidget(self.fournisseur_select)

        # Boutons
        self.add_btn = QPushButton("Ajouter", self)
        self.add_btn.clicked.connect(self.add_medicament)
        layout.addWidget(self.add_btn)

        self.update_btn = QPushButton("Modifier", self)
        self.update_btn.clicked.connect(self.update_medicament)
        layout.addWidget(self.update_btn)

        self.delete_btn = QPushButton("Supprimer", self)
        self.delete_btn.clicked.connect(self.delete_medicament)
        layout.addWidget(self.delete_btn)

        # Table pour afficher les médicaments
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Prix", "Dosage", "Date de Fabrication", "Fournisseur"])
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_medicaments()
        self.table.itemSelectionChanged.connect(self.populate_fields)

    def load_fournisseurs(self):
        fournisseurs = db.fetch_all("SELECT id, nom FROM fournisseur")
        self.fournisseur_select.clear()
        for fournisseur in fournisseurs:
            self.fournisseur_select.addItem(fournisseur[1], fournisseur[0])

    def add_medicament(self):
        nom = self.nom_input.text()
        prix = float(self.prix_input.text())
        dosage = self.dosage_input.text()
        date_fabrication = self.date_fabrication_input.text()
        fournisseur_id = self.fournisseur_select.currentData()

        db.execute_query(
            "INSERT INTO medicament (nom, prix, description, fournisseur_id) VALUES (?, ?, ?, ?)",
            (nom, prix, dosage, fournisseur_id)
        )
        self.load_medicaments()

    def update_medicament(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            return

        id = self.table.item(current_row, 0).text()
        nom = self.nom_input.text()
        prix = float(self.prix_input.text())
        dosage = self.dosage_input.text()
        date_fabrication = self.date_fabrication_input.text()
        fournisseur_id = self.fournisseur_select.currentData()

        db.execute_query(
            "UPDATE medicament SET nom = ?, prix = ?, description = ?, fournisseur_id = ? WHERE id = ?",
            (nom, prix, dosage, fournisseur_id, id)
        )
        self.load_medicaments()

    def delete_medicament(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            return
        id = self.table.item(current_row, 0).text()
        db.execute_query("DELETE FROM medicament WHERE id = ?", (id,))
        self.load_medicaments()

    def load_medicaments(self):
        self.table.setRowCount(0)
        medicaments = db.fetch_all("""
            SELECT m.id, m.nom, m.prix, m.description, m.fournisseur_id, f.nom
            FROM medicament m
            LEFT JOIN fournisseur f ON m.fournisseur_id = f.id
        """)
        for row_idx, row_data in enumerate(medicaments):
            self.table.insertRow(row_idx)
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def populate_fields(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            return

        self.nom_input.setText(self.table.item(current_row, 1).text())
        self.prix_input.setText(self.table.item(current_row, 2).text())
        self.dosage_input.setText(self.table.item(current_row, 3).text())
        self.date_fabrication_input.setText(self.table.item(current_row, 4).text())
        fournisseur_id = self.table.item(current_row, 5).text()

        index = self.fournisseur_select.findText(fournisseur_id)
        if index != -1:
            self.fournisseur_select.setCurrentIndex(index)
