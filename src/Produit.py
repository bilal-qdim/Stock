from Database import Database

class Produit:
    def __init__(self, db_name="gestion_stock.db"):
        self.db = Database(db_name)

    def ajouter_produit(self, nom, quantite, prix):
        query = "INSERT INTO Produit (nom, quantite, prix) VALUES (?, ?, ?)"
        self.db.execute_query(query, (nom, quantite, prix))

    def supprimer_produit(self, produit_id):
        query = "DELETE FROM Produit WHERE id = ?"
        self.db.execute_query(query, (produit_id,))

    def mettre_a_jour_produit(self, produit_id, nom, quantite, prix):
        query = "UPDATE Produit SET nom = ?, quantite = ?, prix = ? WHERE id = ?"
        self.db.execute_query(query, (nom, quantite, prix, produit_id))

    def mettre_a_jour_quantite(self, produit_id, nouvelle_quantite):
        query = "UPDATE Produit SET quantite = ? WHERE id = ?"
        self.db.execute_query(query, (nouvelle_quantite, produit_id))

    def afficher_produits(self):
        query = "SELECT * FROM Produit"
        return self.db.fetch_all(query)

    def get_produit_quantity(self, produit_id):
        query = "SELECT quantite FROM Produit WHERE id = ?"
        result = self.db.fetch_all(query, (produit_id,))
        if result:
            return result[0][0]
        return None
