from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from models import db

class FournisseurUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Fournisseurs")
        self.setGeometry(100, 100, 600, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Champs de saisie
        self.nom_input = QLineEdit(self)
        self.nom_input.setPlaceholderText("Nom")
        self.adresse_input = QLineEdit(self)
        self.adresse_input.setPlaceholderText("Adresse")
        self.telephone_input = QLineEdit(self)
        self.telephone_input.setPlaceholderText("Téléphone")
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.nom_input)
        layout.addWidget(self.adresse_input)
        layout.addWidget(self.telephone_input)
        layout.addWidget(self.email_input)

        # Boutons
        self.add_btn = QPushButton("Ajouter", self)
        self.add_btn.clicked.connect(self.add_fournisseur)
        layout.addWidget(self.add_btn)

        self.update_btn = QPushButton("Modifier", self)
        self.update_btn.clicked.connect(self.update_fournisseur)
        layout.addWidget(self.update_btn)

        self.delete_btn = QPushButton("Supprimer", self)
        self.delete_btn.clicked.connect(self.delete_fournisseur)
        layout.addWidget(self.delete_btn)

        # Table pour afficher les fournisseurs
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Adresse", "Téléphone", "Email"])

        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_fournisseurs()
        self.table.itemSelectionChanged.connect(self.populate_fields)


    def add_fournisseur(self):
        nom = self.nom_input.text()
        adresse = self.adresse_input.text()
        telephone = self.telephone_input.text()
        email = self.email_input.text()
        db.execute_query("INSERT INTO fournisseur (nom, adresse, telephone, email) VALUES (?, ?, ?, ?)",
                         (nom, adresse, telephone, email))
        self.load_fournisseurs()

    def update_fournisseur(self):
    # Vérifier qu'une ligne est sélectionnée
     current_row = self.table.currentRow()
     if current_row == -1:
        return

    # Récupérer l'ID du fournisseur depuis la table
     id = self.table.item(current_row, 0).text()

    # Vérifier que tous les champs sont remplis
     nom = self.nom_input.text().strip()
     adresse = self.adresse_input.text().strip()
     telephone = self.telephone_input.text().strip()
     email = self.email_input.text().strip()

     if not (nom and adresse and telephone):
        print("Veuillez remplir tous les champs obligatoires.")
        return

    # Exécuter la requête de mise à jour
     try:
        db.execute_query(
            "UPDATE fournisseur SET nom = ?, adresse = ?, telephone = ?, email = ? WHERE id = ?",
            (nom, adresse, telephone, email, id)
        )
        print(f"Fournisseur avec ID {id} modifié avec succès.")
     except Exception as e:
        print("Erreur lors de la modification :", e)

    # Recharger les données dans la table
     self.load_fournisseurs()


    def delete_fournisseur(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            return
        id = self.table.item(current_row, 0).text()
        db.execute_query("DELETE FROM fournisseur WHERE id = ?", (id,))
        self.load_fournisseurs()

    def load_fournisseurs(self):
     self.table.setRowCount(0)
    # Charger tous les fournisseurs
     fournisseurs = db.fetch_all("SELECT * FROM fournisseur")
     for row_idx, row_data in enumerate(fournisseurs):
        self.table.insertRow(row_idx)
        for col_idx, col_data in enumerate(row_data):
            self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
    

    def populate_fields(self):
    # Récupérer la ligne sélectionnée
     current_row = self.table.currentRow()
     if current_row == -1:
        return

    # Pré-remplir les champs avec les données de la table
     self.nom_input.setText(self.table.item(current_row, 1).text())
     self.adresse_input.setText(self.table.item(current_row, 2).text())
     self.telephone_input.setText(self.table.item(current_row, 3).text())
     self.email_input.setText(self.table.item(current_row, 4).text() if self.table.item(current_row, 4) else "")
