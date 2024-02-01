import tkinter as tk
from tkinter import ttk
import mysql.connector

# Remplacez les informations de connexion par les vôtres
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nbvcxw.753",
    database="store"
)
cursor = db.cursor()

db.commit()

# Fonction pour mettre à jour la liste des produits dans le tableau
def update_product_list():
    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()
    tree.delete(*tree.get_children())
    for product in products:
        tree.insert("", "end", values=(product[0], product[1], product[2], product[3], product[4], product[5]), tags='center')


# Fonction pour ajouter un nouveau produit
def add_product():
    # Récupérez les valeurs du nouvel élément à partir des widgets d'entrée
    new_name = entry_name.get()
    new_description = entry_description.get()
    new_price = entry_price.get()
    new_quantity = entry_quantity.get()
    new_category = entry_category.get()

    # Effectuez les validations nécessaires
    if not new_quantity.isdigit() or not new_price.isdigit() or not new_name or not new_category:
        # Affichez un message d'erreur ou prenez d'autres mesures nécessaires
        print("Veuillez saisir des valeurs valides pour la quantité, le prix, le nom et la catégorie.")
        return

    # Exécutez la requête SQL pour obtenir l'ID de la catégorie
    cursor.execute("SELECT id FROM category WHERE name = %s", (new_category,))
    category_id = cursor.fetchone()

    if category_id:
        category_id = category_id[0]
    else:
        # Si la catégorie n'existe pas, créez-la
        cursor.execute("INSERT INTO category (name) VALUES (%s)", (new_category,))
        db.commit()
        category_id = cursor.lastrowid

    # Exécutez la requête SQL pour ajouter le nouveau produit
    cursor.execute("""
        INSERT INTO product (name, description, price, quantity, id_category)
        VALUES (%s, %s, %s, %s, %s)
    """, (new_name, new_description, new_price, new_quantity, category_id))

    # Appliquez les changements à la base de données
    db.commit()

    # Mettez à jour la liste des produits dans le tableau
    update_product_list()

    # Effacez les champs d'entrée après l'ajout
    entry_name.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_category.delete(0, tk.END)


# Fonction pour supprimer un produit
def delete_product():
    # Implémentez la logique pour supprimer un produit de la base de données
    # Récupérez l'ID du produit sélectionné dans le tableau
    selected_item = tree.selection()
    if selected_item:
        product_id = tree.item(selected_item, "values")[0]

        # Exécutez la requête SQL pour supprimer le produit
        cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))

        # Appliquez les changements à la base de données
        db.commit()

        # Mettez à jour la liste des produits dans le tableau
        update_product_list()

# Fonction pour modifier un produit
def edit_product():
    # Récupérez l'ID du produit sélectionné dans le tableau
    selected_item = tree.selection()
    if selected_item:
        product_id = tree.item(selected_item, "values")[0]

        # Récupérez les nouvelles valeurs à partir des widgets d'entrée
        new_quantity = entry_edit_quantity.get()
        new_price = entry_edit_price.get()

        # Vérifiez si les champs contiennent des valeurs valides
        if not new_quantity.isdigit() or not new_price.isdigit():
            # Affichez un message d'erreur ou prenez d'autres mesures nécessaires
            print("Veuillez saisir des valeurs valides pour la quantité et le prix.")
            return

        # Exécutez la requête SQL pour mettre à jour le produit
        cursor.execute("""
            UPDATE product
            SET quantity = %s, price = %s
            WHERE id = %s
        """, (new_quantity, new_price, product_id))

        # Appliquez les changements à la base de données
        db.commit()

        # Mettez à jour la liste des produits dans le tableau
        update_product_list()



# Interface graphique
root = tk.Tk()
root.title("Gestion de Stock")

bg_color = "#C0C0C0"  # Orange
fg_color = "#008000"  # Vert foncé
highlight_color = "#FFD700"  # Jaune clair pour mettre en surbrillance les éléments sélectionnés

root.configure(bg=bg_color)

# Tableau de bord
tree = ttk.Treeview(root, columns=("ID", "Nom", "Description", "Prix", "Quantité", "Catégorie"))
tree.heading("#0", text="ID")
tree.heading("#1", text="Nom")
tree.heading("#2", text="Description")
tree.heading("#3", text="Prix")
tree.heading("#4", text="Quantité")
tree.heading("#5", text="Catégorie")

# Configurez la justification pour chaque colonne
column_headers = ["ID", "Nom", "Description", "Prix", "Quantité", "Catégorie"]

for idx, col in enumerate(column_headers):
    tree.column(col, anchor="w")
    tree.heading(col, text=col)



tree.pack()

# Entrées pour ajouter un produit

label_name = tk.Label(root, text="Nom:")
label_name.pack()
entry_name = tk.Entry(root)
entry_name.pack()

label_description = tk.Label(root, text="Description:")
label_description.pack()
entry_description = tk.Entry(root)
entry_description.pack()

label_price = tk.Label(root, text="Prix:")
label_price.pack()
entry_price = tk.Entry(root)
entry_price.pack()

label_quantity = tk.Label(root, text="Quantité:")
label_quantity.pack()
entry_quantity = tk.Entry(root)
entry_quantity.pack()

label_category = tk.Label(root, text="Catégorie:")
label_category.pack()
entry_category = tk.Entry(root)
entry_category.pack()

add_button = tk.Button(root, text="Ajouter", command=add_product)
add_button.pack()


# Entrées pour éditer un produit
edit_frame = tk.Frame(root)
edit_frame.pack()

label_edit_quantity = tk.Label(edit_frame, text="Nouvelle Quantité:")
label_edit_quantity.pack(side=tk.LEFT)
entry_edit_quantity = tk.Entry(edit_frame)
entry_edit_quantity.pack(side=tk.LEFT)

label_edit_price = tk.Label(edit_frame, text="Nouveau Prix:")
label_edit_price.pack(side=tk.LEFT)
entry_edit_price = tk.Entry(edit_frame)
entry_edit_price.pack(side=tk.LEFT)

label_edit_description = tk.Label(edit_frame, text="Nouvelle Description:")
label_edit_description.pack(side=tk.LEFT)
entry_edit_description = tk.Entry(edit_frame)
entry_edit_description.pack(side=tk.LEFT)

edit_button = tk.Button(edit_frame, text="Modifier", command=edit_product)
edit_button.pack()


# Bouton pour supprimer un produit
delete_button = tk.Button(root, text="Supprimer", command=delete_product)
delete_button.pack()

# Mettre à jour la liste des produits lors du lancement de l'application
update_product_list()

root.mainloop()
# Bouton pour supprimer un produit
delete_button = tk.Button(root, text="Supprimer", command=delete_product)
delete_button.pack()

# Mettre à jour la liste des produits lors du lancement de l'application
update_product_list()

root.mainloop()
