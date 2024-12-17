from Database import Database
from Produit import Produit
from datetime import datetime
import wx

class Commande:
    def __init__(self, db_name="gestion_stock.db"):
        self.db = Database(db_name)
        self.db_name = db_name

    def ajouter_commande(self, client_id, produit_id, quantite, date_commande=None):
        if date_commande is None:
            date_commande = datetime.now().strftime("%Y-%m-%d")


        query = """
            INSERT INTO Commande (client_id, produit_id, quantite, date_commande)
            VALUES (?, ?, ?, ?)
        """
        self.db.execute_query(query, (client_id, produit_id, quantite, date_commande))


        produit_manager = Produit(self.db_name)
        current_qte = produit_manager.get_produit_quantity(produit_id)
        if current_qte is not None:
            new_qte = current_qte - quantite
            if new_qte < 0:
                wx.MessageBox("Stock insuffisant! Stock mis à zéro.", "Avertissement", wx.OK | wx.ICON_WARNING)
                new_qte = 0
            produit_manager.mettre_a_jour_quantite(produit_id, new_qte)

    def supprimer_commande(self, commande_id):
        query = "DELETE FROM Commande WHERE id = ?"
        self.db.execute_query(query, (commande_id,))

    def mettre_a_jour_commande(self, commande_id, client_id, produit_id, nouvelle_quantite, date_commande):



        old_data = self.db.fetch_all("SELECT quantite, produit_id FROM Commande WHERE id = ?", (commande_id,))
        if not old_data:
            return

        oldproduitid = old_data[0][1]
        old_quantity = old_data[0][0]



        difference = nouvelle_quantite - old_quantity

        query = """
            UPDATE Commande
            SET client_id = ?, produit_id = ?, quantite = ?, date_commande = ?
            WHERE id = ?
        """
        self.db.execute_query(query, (client_id, produit_id, nouvelle_quantite, date_commande, commande_id))


        produit_manager = Produit(self.db_name)
        current_qte = produit_manager.get_produit_quantity(produit_id)
        if current_qte is not None:
            new_stock = current_qte - difference
            if new_stock < 0:
                wx.MessageBox("Stock insuffisant! Stock mis à zéro.", "Avertissement", wx.OK | wx.ICON_WARNING)
                new_stock = 0
            produit_manager.mettre_a_jour_quantite(produit_id, new_stock)

    def afficher_commandes(self):
        query = "SELECT * FROM Commande"
        return self.db.fetch_all(query)
