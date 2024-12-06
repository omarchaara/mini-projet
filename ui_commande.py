from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox
from models import db
from datetime import datetime

class CommandeUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Commandes")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Champs de saisie
        self.client_input = QLineEdit(self)
        self.client_input.setPlaceholderText("Nom du Client")

        # Champ pour le téléphone
        self.telephone_input = QLineEdit(self)
        self.telephone_input.setPlaceholderText("Numéro de Téléphone du Client")

        self.quantite_input = QLineEdit(self)
        self.quantite_input.setPlaceholderText("Quantité")
        self.date_commande_input = QLineEdit(self)
        self.date_commande_input.setText(datetime.now().strftime("%Y-%m-%d"))
        self.date_commande_input.setPlaceholderText("Date de Commande (AAAA-MM-JJ)")

        # Menu déroulant pour sélectionner un médicament
        self.medicament_select = QComboBox(self)
        self.load_medicaments()

        layout.addWidget(self.client_input)
        layout.addWidget(self.telephone_input)  # Ajout du champ téléphone
        layout.addWidget(self.medicament_select)
        layout.addWidget(self.quantite_input)
        layout.addWidget(self.date_commande_input)

        # Boutons
        self.add_btn = QPushButton("Ajouter", self)
        self.add_btn.clicked.connect(self.add_commande)
        layout.addWidget(self.add_btn)

        self.update_btn = QPushButton("Modifier", self)
        self.update_btn.clicked.connect(self.update_commande)
        layout.addWidget(self.update_btn)

        self.delete_btn = QPushButton("Supprimer", self)
        self.delete_btn.clicked.connect(self.delete_commande)
        layout.addWidget(self.delete_btn)

        # Table pour afficher les commandes
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)  # Une colonne de plus pour le téléphone
        self.table.setHorizontalHeaderLabels(["ID", "Client", "Téléphone", "Médicament", "Quantité", "Total"])
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_commandes()
        self.table.itemSelectionChanged.connect(self.populate_fields)

    def load_medicaments(self):
        medicaments = db.fetch_all("SELECT id, nom FROM medicament")
        self.medicament_select.clear()
        for medicament in medicaments:
            self.medicament_select.addItem(medicament[1], medicament[0])

    def add_commande(self):
        client = self.client_input.text()
        telephone = self.telephone_input.text()  # Récupérer le numéro de téléphone
        medicament_id = self.medicament_select.currentData()
        quantite = int(self.quantite_input.text())
        date_commande = self.date_commande_input.text()

        # Calculer le total
        medicament = db.fetch_one("SELECT prix FROM medicament WHERE id = ?", (medicament_id,))
        total = quantite * medicament[0] if medicament else 0

        db.execute_query(
            "INSERT INTO commande (client, telephone, medicament_id, quantite, date_commande, total) VALUES (?, ?, ?, ?, ?, ?)",
            (client, telephone, medicament_id, quantite, date_commande, total)
        )
        self.load_commandes()

    def update_commande(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            return

        id = self.table.item(current_row, 0).text()
        client = self.client_input.text()
        telephone = self.telephone_input.text()  # Récupérer le téléphone pour la mise à jour
        medicament_id = self.medicament_select.currentData()
        quantite = int(self.quantite_input.text())
        date_commande = self.date_commande_input.text()

        # Calculer le total
        medicament = db.fetch_one("SELECT prix FROM medicament WHERE id = ?", (medicament_id,))
        total = quantite * medicament[0] if medicament else 0

        db.execute_query(
            "UPDATE commande SET client = ?, telephone = ?, medicament_id = ?, quantite = ?, date_commande = ?, total = ? WHERE id = ?",
            (client, telephone, medicament_id, quantite, date_commande, total, id)
        )
        self.load_commandes()

    def delete_commande(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            return
        id = self.table.item(current_row, 0).text()
        db.execute_query("DELETE FROM commande WHERE id = ?", (id,))
        self.load_commandes()

    def load_commandes(self):
        self.table.setRowCount(0)
        commandes = db.fetch_all("""
            SELECT c.id, c.client, c.telephone, m.nom, c.quantite, c.total
            FROM commande c
            LEFT JOIN medicament m ON c.medicament_id = m.id
        """)
        for row_idx, row_data in enumerate(commandes):
            self.table.insertRow(row_idx)
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def populate_fields(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            return

        self.client_input.setText(self.table.item(current_row, 1).text())
        self.telephone_input.setText(self.table.item(current_row, 2).text())  # Remplir le champ téléphone
        self.quantite_input.setText(self.table.item(current_row, 4).text())
        self.date_commande_input.setText(datetime.now().strftime("%Y-%m-%d"))

        medicament_name = self.table.item(current_row, 3).text()
        index = self.medicament_select.findText(medicament_name)
        if index != -1:
            self.medicament_select.setCurrentIndex(index)
