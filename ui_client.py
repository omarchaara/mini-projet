from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from models import db

class ClientUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Clients")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Champ de recherche
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Recherche Client")
        self.search_input.textChanged.connect(self.load_clients)  # Recharger la liste des clients en fonction de la recherche
        layout.addWidget(self.search_input)

        # Table pour afficher les clients
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)  # Colonnes : ID, Nom, Téléphone, Nombre de Commandes, Prix Total, Dernière Commande
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Téléphone", "Nombre de Commandes", "Prix Total", "Dernière Commande"])
        layout.addWidget(self.table)

        # Boutons
        self.modify_btn = QPushButton("Modifier", self)
        self.modify_btn.clicked.connect(self.modify_client)
        layout.addWidget(self.modify_btn)

        self.delete_btn = QPushButton("Supprimer", self)
        self.delete_btn.clicked.connect(self.delete_client)
        layout.addWidget(self.delete_btn)

        self.setLayout(layout)
        self.load_clients()

    def load_clients(self):
     search_text = self.search_input.text()
    # Nouvelle requête SQL avec ROW_NUMBER() pour générer un client_id virtuel
     query = """
        SELECT ROW_NUMBER() OVER (PARTITION BY client, telephone ORDER BY client) AS client_id,
               client, telephone,
               COUNT(id) AS nb_commandes,
               SUM(total) AS total_commandes,
               MAX(date_commande) AS dernier_achat
        FROM commande
        WHERE client LIKE ?
        GROUP BY client, telephone
    """
    
    # Filtre avec le texte de recherche
     clients = db.fetch_all(query, ('%' + search_text + '%',))  # Appliquer le filtre de recherche
     self.table.setRowCount(0)

    # Remplissage de la table avec les données récupérées
     for row_idx, row_data in enumerate(clients):
        self.table.insertRow(row_idx)
        for col_idx, col_data in enumerate(row_data):
            self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))





    def modify_client(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            return

        # Récupérer les informations du client sélectionné
        client_id = self.table.item(current_row, 0).text()
        client_nom = self.table.item(current_row, 1).text()
        client_telephone = self.table.item(current_row, 2).text()

        # Ouvrir une fenêtre de modification (ou un simple QLineEdit pour modifier directement)
        # Vous pouvez implémenter une autre fenêtre pop-up pour la modification
        print(f"Modifier le client: {client_nom}, {client_telephone}, ID: {client_id}")
        # Vous pouvez créer une autre fenêtre ou faire une modification en place dans ce code
        # Exemple: self.modify_client_window(client_id)

    def delete_client(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            return
        client_id = self.table.item(current_row, 0).text()

        # Supprimer le client
        db.execute_query("DELETE FROM client WHERE id = ?", (client_id,))
        self.load_clients()
