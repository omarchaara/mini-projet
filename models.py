import sqlite3

# Classe de gestion de la base de données
class DatabaseManager:
    def __init__(self, db_name="database.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
     with self.connection:
        # Table des fournisseurs
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS fournisseur (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                adresse TEXT NOT NULL,
                telephone TEXT NOT NULL,
                email TEXT
            )
        """)
        # Table des médicaments
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS medicament (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                description TEXT,
                prix REAL NOT NULL,
                fournisseur_id INTEGER,
                FOREIGN KEY (fournisseur_id) REFERENCES fournisseur (id)
            )
        """)
        # Supprimer l'ancienne table commande (si nécessaire)
        self.connection.execute("DROP TABLE IF EXISTS commande")
        
        # Nouvelle table des commandes avec un champ telephone
        self.connection.execute("""
                CREATE TABLE IF NOT EXISTS commande (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client TEXT NOT NULL,
                    telephone TEXT NOT NULL,
                    medicament_id INTEGER,
                    quantite INTEGER NOT NULL,
                    date_commande TEXT NOT NULL,
                    total REAL NOT NULL,
                    FOREIGN KEY (medicament_id) REFERENCES medicament (id)
                )
            """)
     

      # Table des clients
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS client (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                telephone TEXT NOT NULL
            )
        """)



    def execute_query(self, query, params=()):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor

    def fetch_all(self, query, params=()):
        return self.execute_query(query, params).fetchall()

    def fetch_one(self, query, params=()):
        return self.execute_query(query, params).fetchone()

db = DatabaseManager()
