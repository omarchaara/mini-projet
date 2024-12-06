from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from ui_fournisseur import FournisseurUI
from ui_medicament import MedicamentUI
from ui_commande import CommandeUI
from ui_client import ClientUI


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Entités")
        self.setGeometry(100, 100, 300, 200)
        self.setup_ui()

        # Références aux interfaces
        self.fournisseur_ui = None
        self.medicament_ui = None
        self.commande_ui = None
        self.client_ui = None  # Ajout de la référence pour l'interface client

    def setup_ui(self):
        layout = QVBoxLayout()

        # Bouton pour ouvrir l'interface client
        self.client_btn = QPushButton("Gestion des Clients", self)
        self.client_btn.clicked.connect(self.open_client_ui)
        layout.addWidget(self.client_btn)

        # Bouton pour gérer les commandes
        self.commande_btn = QPushButton("Gestion des Commandes", self)
        self.commande_btn.clicked.connect(self.open_commande_ui)
        layout.addWidget(self.commande_btn)

        # Bouton pour gérer les fournisseurs
        self.fournisseur_btn = QPushButton("Gestion des Fournisseurs", self)
        self.fournisseur_btn.clicked.connect(self.open_fournisseur_ui)
        layout.addWidget(self.fournisseur_btn)

        # Bouton pour gérer les médicaments
        self.medicament_btn = QPushButton("Gestion des Médicaments", self)
        self.medicament_btn.clicked.connect(self.open_medicament_ui)
        layout.addWidget(self.medicament_btn)

        self.setLayout(layout)

    def open_fournisseur_ui(self):
        if not self.fournisseur_ui:
            self.fournisseur_ui = FournisseurUI()
            self.fournisseur_ui.closeEvent = self.close_fournisseur_ui
            self.fournisseur_ui.show()

    def open_medicament_ui(self):
        if not self.medicament_ui:
            self.medicament_ui = MedicamentUI()
            self.medicament_ui.closeEvent = self.close_medicament_ui
            self.medicament_ui.show()

    def open_commande_ui(self):
        if not self.commande_ui:
            self.commande_ui = CommandeUI()
            self.commande_ui.closeEvent = self.close_commande_ui
            self.commande_ui.show()

    def open_client_ui(self):
        if not self.client_ui:  # Vérifier si l'interface client est déjà ouverte
            self.client_ui = ClientUI()
            self.client_ui.closeEvent = self.close_client_ui  # Associer l'événement de fermeture
            self.client_ui.show()

    # Méthodes de fermeture pour gérer l'instance
    def close_fournisseur_ui(self, event):
        self.fournisseur_ui = None
        event.accept()

    def close_medicament_ui(self, event):
        self.medicament_ui = None
        event.accept()

    def close_commande_ui(self, event):
        self.commande_ui = None
        event.accept()

    def close_client_ui(self, event):
        self.client_ui = None
        event.accept()
