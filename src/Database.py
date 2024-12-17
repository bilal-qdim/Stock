import sqlite3

class Database:
    def __init__(self, db_name="gestion_stock.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

    @staticmethod
    def initialize_db(db_name="gestion_stock.db"):
        db = Database(db_name)

        db.execute_query('''
            CREATE TABLE IF NOT EXISTS Client (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')

        db.execute_query('''
            CREATE TABLE IF NOT EXISTS Produit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                quantite INTEGER NOT NULL,
                prix REAL NOT NULL
            )
        ''')

        db.execute_query('''
            CREATE TABLE IF NOT EXISTS Fournisseur (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                contact TEXT
            )
        ''')

        db.execute_query('''
            CREATE TABLE IF NOT EXISTS Commande (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER,
                produit_id INTEGER,
                quantite INTEGER NOT NULL,
                date_commande TEXT,
                FOREIGN KEY (client_id) REFERENCES Client (id),
                FOREIGN KEY (produit_id) REFERENCES Produit (id)
            )
        ''')

        db.close()
