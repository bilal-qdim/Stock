from Database import Database

class Client:
    def __init__(self, db_name="gestion_stock.db"):
        self.db = Database(db_name)

    def ajouter_client(self, nom, prenom, email):
        query = "INSERT INTO Client (nom, prenom, email) VALUES (?, ?, ?)"
        self.db.execute_query(query, (nom, prenom, email))

    def supprimer_client(self, client_id):
        query = "DELETE FROM Client WHERE id = ?"
        self.db.execute_query(query, (client_id,))

    def mettre_a_jour_client(self, client_id, nom, prenom, email):
        query = "UPDATE Client SET nom = ?, prenom = ?, email = ? WHERE id = ?"
        self.db.execute_query(query, (nom, prenom, email, client_id))

    def afficher_clients(self):
        query = "SELECT * FROM Client"
        return self.db.fetch_all(query)
