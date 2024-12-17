from Database import Database

class Fournisseur:
    def __init__(self, db_name="gestion_stock.db"):
        self.db = Database(db_name)

    def ajouter_fournisseur(self, nom, contact):
        query = "INSERT INTO Fournisseur (nom, contact) VALUES (?, ?)"
        self.db.execute_query(query, (nom, contact))

    def supprimer_fournisseur(self, fournisseur_id):
        query = "DELETE FROM Fournisseur WHERE id = ?"
        self.db.execute_query(query, (fournisseur_id,))

    def mettre_a_jour_fournisseur(self, fournisseur_id, nom, contact):
        query = "UPDATE Fournisseur SET nom = ?, contact = ? WHERE id = ?"
        self.db.execute_query(query, (nom, contact, fournisseur_id))

    def afficher_fournisseurs(self):
        query = "SELECT * FROM Fournisseur"
        return self.db.fetch_all(query)
