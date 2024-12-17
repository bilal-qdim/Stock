import wx
from Database import Database
from Client import Client
from Produit import Produit
from Fournisseur import Fournisseur
from Commande import Commande
from datetime import datetime

class GestionStockApp(wx.Frame):
    def __init__(self, db_name="gestion_stock.db"):
        super().__init__(None, title="Gestion de Stock", size=(900, 550))

        Database.initialize_db(db_name)

        self.client_manager = Client(db_name)
        self.produit_manager = Produit(db_name)
        self.fournisseur_manager = Fournisseur(db_name)
        self.commande_manager = Commande(db_name)

        self.selected_client_id = None
        self.selected_produit_id = None
        self.selected_fournisseur_id = None
        self.selected_commande_id = None

        panel = wx.Panel(self)
        notebook = wx.Notebook(panel)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(notebook, 1, wx.EXPAND)


        client_panel = wx.Panel(notebook)
        client_sizer = wx.BoxSizer(wx.VERTICAL)

        form_sizer = wx.FlexGridSizer(rows=3, cols=2, hgap=5, vgap=5)
        form_sizer.AddGrowableCol(1, 1)

        self.nom_text = wx.TextCtrl(client_panel)
        self.prenom_text = wx.TextCtrl(client_panel)
        self.email_text = wx.TextCtrl(client_panel)

        form_sizer.Add(wx.StaticText(client_panel, label="Nom :"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        form_sizer.Add(self.nom_text, 1, wx.EXPAND | wx.ALL, 5)
        form_sizer.Add(wx.StaticText(client_panel, label="Prénom :"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        form_sizer.Add(self.prenom_text, 1, wx.EXPAND | wx.ALL, 5)
        form_sizer.Add(wx.StaticText(client_panel, label="Email :"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        form_sizer.Add(self.email_text, 1, wx.EXPAND | wx.ALL, 5)

        client_sizer.Add(form_sizer, 0, wx.EXPAND | wx.ALL, 10)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        add_client_btn = wx.Button(client_panel, label="Ajouter")
        add_client_btn.Bind(wx.EVT_BUTTON, self.on_ajouter_client)
        btn_sizer.Add(add_client_btn, 0, wx.ALL, 5)

        update_client_btn = wx.Button(client_panel, label="Mettre à jour")
        update_client_btn.Bind(wx.EVT_BUTTON, self.on_update_client)
        btn_sizer.Add(update_client_btn, 0, wx.ALL, 5)

        delete_client_btn = wx.Button(client_panel, label="Supprimer")
        delete_client_btn.Bind(wx.EVT_BUTTON, self.on_delete_client)
        btn_sizer.Add(delete_client_btn, 0, wx.ALL, 5)

        client_sizer.Add(btn_sizer, 0, wx.ALL | wx.CENTER, 5)

        self.liste_clients = wx.ListCtrl(client_panel, style=wx.LC_REPORT)
        self.liste_clients.InsertColumn(0, "ID", width=50)
        self.liste_clients.InsertColumn(1, "Nom", width=120)
        self.liste_clients.InsertColumn(2, "Prénom", width=120)
        self.liste_clients.InsertColumn(3, "Email", width=200)
        self.liste_clients.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_client_selected)

        client_sizer.Add(self.liste_clients, 1, wx.EXPAND | wx.ALL, 10)
        client_panel.SetSizer(client_sizer)
        notebook.AddPage(client_panel, "Clients")


        produit_panel = wx.Panel(notebook)
        produit_sizer = wx.BoxSizer(wx.VERTICAL)

        form_produit_sizer = wx.FlexGridSizer(rows=3, cols=2, hgap=5, vgap=5)
        form_produit_sizer.AddGrowableCol(1, 1)

        self.nom_produit_text = wx.TextCtrl(produit_panel)
        self.quantite_produit_text = wx.TextCtrl(produit_panel)
        self.prix_produit_text = wx.TextCtrl(produit_panel)

        form_produit_sizer.Add(wx.StaticText(produit_panel, label="Nom :"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        form_produit_sizer.Add(self.nom_produit_text, 1, wx.EXPAND | wx.ALL, 5)
        form_produit_sizer.Add(wx.StaticText(produit_panel, label="Quantité :"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        form_produit_sizer.Add(self.quantite_produit_text, 1, wx.EXPAND | wx.ALL, 5)
        form_produit_sizer.Add(wx.StaticText(produit_panel, label="Prix :"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        form_produit_sizer.Add(self.prix_produit_text, 1, wx.EXPAND | wx.ALL, 5)

        produit_sizer.Add(form_produit_sizer, 0, wx.EXPAND | wx.ALL, 10)

        produit_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        add_produit_btn = wx.Button(produit_panel, label="Ajouter")
        add_produit_btn.Bind(wx.EVT_BUTTON, self.on_ajouter_produit)
        produit_btn_sizer.Add(add_produit_btn, 0, wx.ALL, 5)

        update_produit_btn = wx.Button(produit_panel, label="Mettre à jour")
        update_produit_btn.Bind(wx.EVT_BUTTON, self.on_update_produit)
        produit_btn_sizer.Add(update_produit_btn, 0, wx.ALL, 5)

        delete_produit_btn = wx.Button(produit_panel, label="Supprimer")
        delete_produit_btn.Bind(wx.EVT_BUTTON, self.on_delete_produit)
        produit_btn_sizer.Add(delete_produit_btn, 0, wx.ALL, 5)

        produit_sizer.Add(produit_btn_sizer, 0, wx.ALL | wx.CENTER, 5)

        self.liste_produits = wx.ListCtrl(produit_panel, style=wx.LC_REPORT)
        self.liste_produits.InsertColumn(0, "ID", width=50)
        self.liste_produits.InsertColumn(1, "Nom", width=150)
        self.liste_produits.InsertColumn(2, "Quantité", width=80)
        self.liste_produits.InsertColumn(3, "Prix", width=80)
        self.liste_produits.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_produit_selected)

        produit_sizer.Add(self.liste_produits, 1, wx.EXPAND | wx.ALL, 10)
        produit_panel.SetSizer(produit_sizer)
        notebook.AddPage(produit_panel, "Produits")


        fournisseur_panel = wx.Panel(notebook)
        fournisseur_sizer = wx.BoxSizer(wx.VERTICAL)

        form_fournisseur_sizer = wx.FlexGridSizer(rows=2, cols=2, hgap=5, vgap=5)
        form_fournisseur_sizer.AddGrowableCol(1, 1)

        self.nom_fournisseur_text = wx.TextCtrl(fournisseur_panel)
        self.contact_fournisseur_text = wx.TextCtrl(fournisseur_panel)

        form_fournisseur_sizer.Add(wx.StaticText(fournisseur_panel, label="Nom :"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        form_fournisseur_sizer.Add(self.nom_fournisseur_text, 1, wx.EXPAND | wx.ALL, 5)
        form_fournisseur_sizer.Add(wx.StaticText(fournisseur_panel, label="Contact :"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        form_fournisseur_sizer.Add(self.contact_fournisseur_text, 1, wx.EXPAND | wx.ALL, 5)

        fournisseur_sizer.Add(form_fournisseur_sizer, 0, wx.EXPAND | wx.ALL, 10)

        fournisseur_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        add_fournisseur_btn = wx.Button(fournisseur_panel, label="Ajouter")
        add_fournisseur_btn.Bind(wx.EVT_BUTTON, self.on_ajouter_fournisseur)
        fournisseur_btn_sizer.Add(add_fournisseur_btn, 0, wx.ALL, 5)

        update_fournisseur_btn = wx.Button(fournisseur_panel, label="Mettre à jour")
        update_fournisseur_btn.Bind(wx.EVT_BUTTON, self.on_update_fournisseur)
        fournisseur_btn_sizer.Add(update_fournisseur_btn, 0, wx.ALL, 5)

        delete_fournisseur_btn = wx.Button(fournisseur_panel, label="Supprimer")
        delete_fournisseur_btn.Bind(wx.EVT_BUTTON, self.on_delete_fournisseur)
        fournisseur_btn_sizer.Add(delete_fournisseur_btn, 0, wx.ALL, 5)

        fournisseur_sizer.Add(fournisseur_btn_sizer, 0, wx.ALL | wx.CENTER, 5)

        self.liste_fournisseurs = wx.ListCtrl(fournisseur_panel, style=wx.LC_REPORT)
        self.liste_fournisseurs.InsertColumn(0, "ID", width=50)
        self.liste_fournisseurs.InsertColumn(1, "Nom", width=150)
        self.liste_fournisseurs.InsertColumn(2, "Contact", width=150)
        self.liste_fournisseurs.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_fournisseur_selected)

        fournisseur_sizer.Add(self.liste_fournisseurs, 1, wx.EXPAND | wx.ALL, 10)
        fournisseur_panel.SetSizer(fournisseur_sizer)
        notebook.AddPage(fournisseur_panel, "Fournisseurs")


        commande_panel = wx.Panel(notebook)
        commande_sizer = wx.BoxSizer(wx.VERTICAL)

        form_commande_sizer = wx.FlexGridSizer(rows=4, cols=2, hgap=5, vgap=5)
        form_commande_sizer.AddGrowableCol(1, 1)

        self.client_id_text = wx.TextCtrl(commande_panel)
        self.produit_id_text = wx.TextCtrl(commande_panel)
        self.quantite_commande_text = wx.TextCtrl(commande_panel)
        self.date_commande_text = wx.TextCtrl(commande_panel)

        form_commande_sizer.Add(wx.StaticText(commande_panel, label="Client ID :"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        form_commande_sizer.Add(self.client_id_text, 1, wx.EXPAND | wx.ALL, 5)
        form_commande_sizer.Add(wx.StaticText(commande_panel, label="Produit ID :"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        form_commande_sizer.Add(self.produit_id_text, 1, wx.EXPAND | wx.ALL, 5)
        form_commande_sizer.Add(wx.StaticText(commande_panel, label="Quantité :"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        form_commande_sizer.Add(self.quantite_commande_text, 1, wx.EXPAND | wx.ALL, 5)
        form_commande_sizer.Add(wx.StaticText(commande_panel, label="Date (YYYY-MM-DD) :"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        form_commande_sizer.Add(self.date_commande_text, 1, wx.EXPAND | wx.ALL, 5)

        commande_sizer.Add(form_commande_sizer, 0, wx.EXPAND | wx.ALL, 10)

        commande_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        add_commande_btn = wx.Button(commande_panel, label="Ajouter")
        add_commande_btn.Bind(wx.EVT_BUTTON, self.on_ajouter_commande)
        commande_btn_sizer.Add(add_commande_btn, 0, wx.ALL, 5)

        update_commande_btn = wx.Button(commande_panel, label="Mettre à jour")
        update_commande_btn.Bind(wx.EVT_BUTTON, self.on_update_commande)
        commande_btn_sizer.Add(update_commande_btn, 0, wx.ALL, 5)

        delete_commande_btn = wx.Button(commande_panel, label="Supprimer")
        delete_commande_btn.Bind(wx.EVT_BUTTON, self.on_delete_commande)
        commande_btn_sizer.Add(delete_commande_btn, 0, wx.ALL, 5)

        commande_sizer.Add(commande_btn_sizer, 0, wx.ALL | wx.CENTER, 5)

        self.liste_commandes = wx.ListCtrl(commande_panel, style=wx.LC_REPORT)
        self.liste_commandes.InsertColumn(0, "ID", width=50)
        self.liste_commandes.InsertColumn(1, "Client ID", width=80)
        self.liste_commandes.InsertColumn(2, "Produit ID", width=80)
        self.liste_commandes.InsertColumn(3, "Quantité", width=80)
        self.liste_commandes.InsertColumn(4, "Date", width=100)
        self.liste_commandes.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_commande_selected)

        commande_sizer.Add(self.liste_commandes, 1, wx.EXPAND | wx.ALL, 10)
        commande_panel.SetSizer(commande_sizer)
        notebook.AddPage(commande_panel, "Commandes")

        panel.SetSizer(main_sizer)

        # Populate lists
        self.update_client_list()
        self.update_produit_list()
        self.update_fournisseur_list()
        self.update_commande_list()

        self.Show()

    def on_ajouter_client(self, event):
        nom = self.nom_text.GetValue()
        prenom = self.prenom_text.GetValue()
        email = self.email_text.GetValue()
        if nom and prenom and email:
            self.client_manager.ajouter_client(nom, prenom, email)
            wx.MessageBox("Client ajouté avec succès!", "Info", wx.OK | wx.ICON_INFORMATION)
            self.update_client_list()
            self.nom_text.SetValue("")
            self.prenom_text.SetValue("")
            self.email_text.SetValue("")
            self.selected_client_id = None
        else:
            wx.MessageBox("Veuillez remplir tous les champs.", "Erreur", wx.OK | wx.ICON_ERROR)

    def on_update_client(self, event):
        if self.selected_client_id is None:
            wx.MessageBox("Veuillez sélectionner un client.", "Erreur", wx.OK | wx.ICON_ERROR)
            return
        nom = self.nom_text.GetValue()
        prenom = self.prenom_text.GetValue()
        email = self.email_text.GetValue()
        if nom and prenom and email:
            self.client_manager.mettre_a_jour_client(self.selected_client_id, nom, prenom, email)
            wx.MessageBox("Client mis à jour avec succès!", "Info", wx.OK | wx.ICON_INFORMATION)
            self.update_client_list()
        else:
            wx.MessageBox("Champs invalides pour la mise à jour.", "Erreur", wx.OK | wx.ICON_ERROR)

    def on_delete_client(self, event):
        if self.selected_client_id is None:
            wx.MessageBox("Veuillez sélectionner un client à supprimer.", "Erreur", wx.OK | wx.ICON_ERROR)
            return
        self.client_manager.supprimer_client(self.selected_client_id)
        wx.MessageBox("Client supprimé avec succès!", "Info", wx.OK | wx.ICON_INFORMATION)
        self.update_client_list()
        self.selected_client_id = None

    def on_client_selected(self, event):
        index = event.GetIndex()
        self.selected_client_id = int(self.liste_clients.GetItemText(index, 0))
        self.nom_text.SetValue(self.liste_clients.GetItemText(index, 1))
        self.prenom_text.SetValue(self.liste_clients.GetItemText(index, 2))
        self.email_text.SetValue(self.liste_clients.GetItemText(index, 3))

    def update_client_list(self):
        self.liste_clients.DeleteAllItems()
        clients = self.client_manager.afficher_clients()
        for c in clients:
            idx = self.liste_clients.InsertItem(self.liste_clients.GetItemCount(), str(c[0]))
            self.liste_clients.SetItem(idx, 1, str(c[1]))
            self.liste_clients.SetItem(idx, 2, str(c[2]))
            self.liste_clients.SetItem(idx, 3, str(c[3]))


    def on_ajouter_produit(self, event):
        nom = self.nom_produit_text.GetValue()
        quantite = self.quantite_produit_text.GetValue()
        prix = self.prix_produit_text.GetValue()

        if nom and quantite.isdigit() and prix:
            self.produit_manager.ajouter_produit(nom, int(quantite), float(prix))
            wx.MessageBox("Produit ajouté avec succès!", "Info", wx.OK | wx.ICON_INFORMATION)
            self.update_produit_list()
            self.nom_produit_text.SetValue("")
            self.quantite_produit_text.SetValue("")
            self.prix_produit_text.SetValue("")
            self.selected_produit_id = None
        else:
            wx.MessageBox("Champs invalides (quantité doit être un entier, prix un nombre).", "Erreur", wx.OK | wx.ICON_ERROR)

    def on_update_produit(self, event):
        if self.selected_produit_id is None:
            wx.MessageBox("Veuillez sélectionner un produit.", "Erreur", wx.OK | wx.ICON_ERROR)
            return

        nom = self.nom_produit_text.GetValue()
        quantite = self.quantite_produit_text.GetValue()
        prix = self.prix_produit_text.GetValue()

        if nom and quantite.isdigit() and prix:
            self.produit_manager.mettre_a_jour_produit(self.selected_produit_id, nom, int(quantite), float(prix))
            wx.MessageBox("Produit mis à jour avec succès!", "Info", wx.OK | wx.ICON_INFORMATION)
            self.update_produit_list()
        else:
            wx.MessageBox("Champs invalides pour la mise à jour.", "Erreur", wx.OK | wx.ICON_ERROR)

    def on_delete_produit(self, event):
        if self.selected_produit_id is None:
            wx.MessageBox("Veuillez sélectionner un produit à supprimer.", "Erreur", wx.OK | wx.ICON_ERROR)
            return
        self.produit_manager.supprimer_produit(self.selected_produit_id)
        wx.MessageBox("Produit supprimé avec succès!", "Info", wx.OK | wx.ICON_INFORMATION)
        self.update_produit_list()
        self.selected_produit_id = None

    def on_produit_selected(self, event):
        index = event.GetIndex()
        self.selected_produit_id = int(self.liste_produits.GetItemText(index, 0))
        self.nom_produit_text.SetValue(self.liste_produits.GetItemText(index, 1))
        self.quantite_produit_text.SetValue(self.liste_produits.GetItemText(index, 2))
        self.prix_produit_text.SetValue(self.liste_produits.GetItemText(index, 3))

    def update_produit_list(self):
        self.liste_produits.DeleteAllItems()
        produits = self.produit_manager.afficher_produits()
        for p in produits:
            idx = self.liste_produits.InsertItem(self.liste_produits.GetItemCount(), str(p[0]))
            self.liste_produits.SetItem(idx, 1, str(p[1]))
            self.liste_produits.SetItem(idx, 2, str(p[2]))
            self.liste_produits.SetItem(idx, 3, str(p[3]))


    def on_ajouter_fournisseur(self, event):
        nom = self.nom_fournisseur_text.GetValue()
        contact = self.contact_fournisseur_text.GetValue()

        if nom:
            self.fournisseur_manager.ajouter_fournisseur(nom, contact)
            wx.MessageBox("Fournisseur ajouté avec succès!", "Info", wx.OK | wx.ICON_INFORMATION)
            self.update_fournisseur_list()
            self.nom_fournisseur_text.SetValue("")
            self.contact_fournisseur_text.SetValue("")
            self.selected_fournisseur_id = None
        else:
            wx.MessageBox("Le nom du fournisseur est obligatoire.", "Erreur", wx.OK | wx.ICON_ERROR)

    def on_update_fournisseur(self, event):
        if self.selected_fournisseur_id is None:
            wx.MessageBox("Veuillez sélectionner un fournisseur.", "Erreur", wx.OK | wx.ICON_ERROR)
            return
        nom = self.nom_fournisseur_text.GetValue()
        contact = self.contact_fournisseur_text.GetValue()

        if nom:
            self.fournisseur_manager.mettre_a_jour_fournisseur(self.selected_fournisseur_id, nom, contact)
            wx.MessageBox("Fournisseur mis à jour avec succès!", "Info", wx.OK | wx.ICON_INFORMATION)
            self.update_fournisseur_list()
        else:
            wx.MessageBox("Champs invalides pour la mise à jour.", "Erreur", wx.OK | wx.ICON_ERROR)

    def on_delete_fournisseur(self, event):
        if self.selected_fournisseur_id is None:
            wx.MessageBox("Veuillez sélectionner un fournisseur à supprimer.", "Erreur", wx.OK | wx.ICON_ERROR)
            return
        self.fournisseur_manager.supprimer_fournisseur(self.selected_fournisseur_id)
        wx.MessageBox("Fournisseur supprimé avec succès!", "Info", wx.OK | wx.ICON_INFORMATION)
        self.update_fournisseur_list()
        self.selected_fournisseur_id = None

    def on_fournisseur_selected(self, event):
        index = event.GetIndex()
        self.selected_fournisseur_id = int(self.liste_fournisseurs.GetItemText(index, 0))
        self.nom_fournisseur_text.SetValue(self.liste_fournisseurs.GetItemText(index, 1))
        self.contact_fournisseur_text.SetValue(self.liste_fournisseurs.GetItemText(index, 2))

    def update_fournisseur_list(self):
        self.liste_fournisseurs.DeleteAllItems()
        fournisseurs = self.fournisseur_manager.afficher_fournisseurs()
        for f in fournisseurs:
            idx = self.liste_fournisseurs.InsertItem(self.liste_fournisseurs.GetItemCount(), str(f[0]))
            self.liste_fournisseurs.SetItem(idx, 1, str(f[1]))
            self.liste_fournisseurs.SetItem(idx, 2, str(f[2]))


    def on_ajouter_commande(self, event):
        client_id = self.client_id_text.GetValue()
        produit_id = self.produit_id_text.GetValue()
        quantite = self.quantite_commande_text.GetValue()
        date_commande = self.date_commande_text.GetValue() or None

        if client_id.isdigit() and produit_id.isdigit() and quantite.isdigit():
            self.commande_manager.ajouter_commande(int(client_id), int(produit_id), int(quantite), date_commande)
            wx.MessageBox("Commande ajoutée, stock mis à jour!", "Info", wx.OK | wx.ICON_INFORMATION)
            self.update_commande_list()
            self.client_id_text.SetValue("")
            self.produit_id_text.SetValue("")
            self.quantite_commande_text.SetValue("")
            self.date_commande_text.SetValue("")
            self.selected_commande_id = None
        else:
            wx.MessageBox("Client ID, Produit ID, et Quantité doivent être des entiers!",
                          "Erreur", wx.OK | wx.ICON_ERROR)

    def on_update_commande(self, event):
        if self.selected_commande_id is None:
            wx.MessageBox("Veuillez sélectionner une commande.", "Erreur", wx.OK | wx.ICON_ERROR)
            return

        client_id = self.client_id_text.GetValue()
        produit_id = self.produit_id_text.GetValue()
        quantite = self.quantite_commande_text.GetValue()
        date_commande = self.date_commande_text.GetValue() or datetime.now().strftime("%Y-%m-%d")

        if client_id.isdigit() and produit_id.isdigit() and quantite.isdigit():
            self.commande_manager.mettre_a_jour_commande(
                self.selected_commande_id,
                int(client_id),
                int(produit_id),
                int(quantite),
                date_commande
            )
            wx.MessageBox("Commande mise à jour, stock auto-ajusté!", "Info", wx.OK | wx.ICON_INFORMATION)
            self.update_commande_list()
        else:
            wx.MessageBox("Tous les champs doivent être valides (entiers).", "Erreur", wx.OK | wx.ICON_ERROR)

    def on_delete_commande(self, event):
        if self.selected_commande_id is None:
            wx.MessageBox("Veuillez sélectionner une commande à supprimer.", "Erreur", wx.OK | wx.ICON_ERROR)
            return
        self.commande_manager.supprimer_commande(self.selected_commande_id)
        wx.MessageBox("Commande supprimée!", "Info", wx.OK | wx.ICON_INFORMATION)
        self.update_commande_list()
        self.selected_commande_id = None

    def on_commande_selected(self, event):
        index = event.GetIndex()
        self.selected_commande_id = int(self.liste_commandes.GetItemText(index, 0))
        self.client_id_text.SetValue(self.liste_commandes.GetItemText(index, 1))
        self.produit_id_text.SetValue(self.liste_commandes.GetItemText(index, 2))
        self.quantite_commande_text.SetValue(self.liste_commandes.GetItemText(index, 3))
        self.date_commande_text.SetValue(self.liste_commandes.GetItemText(index, 4))

    def update_commande_list(self):
        self.liste_commandes.DeleteAllItems()
        commandes = self.commande_manager.afficher_commandes()
        for cmd in commandes:
            idx = self.liste_commandes.InsertItem(self.liste_commandes.GetItemCount(), str(cmd[0]))
            self.liste_commandes.SetItem(idx, 1, str(cmd[1]))
            self.liste_commandes.SetItem(idx, 2, str(cmd[2]))
            self.liste_commandes.SetItem(idx, 3, str(cmd[3]))
            self.liste_commandes.SetItem(idx, 4, str(cmd[4]))

if __name__ == "__main__":
    app = wx.App(False)
    frame = GestionStockApp("gestion_stock.db")
    app.MainLoop()
