import sqlite3

class Product:
    def __init__(self):
        self.connection = sqlite3.connect('./db/stock.db')
        self.cursor = self.connection.cursor()
        print("Successfully Connected to SQLite")
        self._create_table()

    def __del__(self):
        print("Super destructeur called")
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def __str__(self):
        """
        Returns a string representation of the inventory.
        Returns:
            str: The inventory items and their quantities sold.
        """
        new_bilan = "{:<15} | {:<5} | {}\n".format("Name", "Stock", "Price")
        rows = self.read_table()
        for key in rows:
            new_bilan += "{:<15} | {:<5} | {}\n".format(key[0], key[1], key[2])
        return new_bilan

    def _create_table(self):
        """
        Crée une table 'products' dans la base de données SQLite si elle
        n'existe pas déjà.
        Cette fonction ne prend pas de paramètres.
        Elle exécute la requête SQL de création de table et commit les
        modifications.
        """
        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS products(
                            name TEXT NOT NULL PRIMARY KEY,
                            stockQty INTEGER,
                            sellPrice REAL);'''
        self.cursor.execute(sqlite_create_table_query)
        self.connection.commit()

    def _update_buy(self, name: str, newQty:int):
        """
        Met à jour la quantité de stock d'un produit dans la table 'products'.
        :param name: Le nom du produit à mettre à jour.
        :type name: str
        :param newQty: La nouvelle quantité de stock pour le produit.
        :type newQty: int
        Cette fonction exécute la requête SQL pour mettre à jour la quantité
        de stock du produit spécifié et commit les modifications.
        """
        data = (newQty, name)
        sql_update_query = """Update products set stockQty = ? where name = ?"""
        self.cursor.execute(sql_update_query, data)
        self.connection.commit()

    def _get_row_by_name(self, search: str)-> tuple:
        """
        Récupère la première ligne de la table 'products' correspondant au nom
        de produit spécifié.
        :param search: Le nom du produit à rechercher.
        :type search: str
        :return: Un tuple représentant la première ligne correspondante dans
                 la table 'products', ou None si aucune correspondance n'est
                 trouvée.
        :rtype: tuple or None
        Cette fonction exécute la requête SQL de recherche et retourne
        la première ligne correspondante sous forme de tuple.
        """
        sqlite_select_query = """ SELECT * from products where name = ?"""
        self.cursor.execute(sqlite_select_query, (search.lower(),))
        record = self.cursor.fetchall()
        if (record):
            return (record[0])
        return 
    
    def read_table(self)-> tuple:
        """
        Return all the ligne of the table 'products'.
        This function doesn't take any parameters.
        :return: A tuple with all the lines of the table 'products'.
        :rtype: tuple
        This function execute a sql query to get all the lines in the table
        'products' and return it as a tuple
        """
        sqlite_select_query = """ SELECT * from products"""
        self.cursor.execute(sqlite_select_query)
        rows = self.cursor.fetchall()
        return (rows)

    def add_item(self, name: str, stock: int, sellPrice: float):
        """
        Adds items to the stockDB .
        Args:
            name (str): The name of the item to add.
            stock (int): The quantity of the item to add.
            sellQty (int): the quantity that was sold since last time
            sellPrice (float): the price of the item that is add
        """
        if (stock < 0 or sellPrice < 0):
            return -1
        item = (name.lower(), stock, sellPrice)
        if (self._get_row_by_name(name.lower())):
            return 1
        sqlite_insert_query = """INSERT OR IGNORE INTO products(
                            name, stockQty, sellPrice)
                            VALUES (?, ?, ?);"""
        self.cursor.execute(sqlite_insert_query, item)
        self.connection.commit()
        return 0

    def achat_item(self, nameup: str, qty: int = 1):
        """
        An item has been sold qty time
        Args:
            nameup (str): The name of the item.
            qty (int): The quantity to add to the quantity sold. Default is 1.
        """
        item = self._get_row_by_name(nameup)
        if (not item):
            return 1
        if (qty <= 0):
            return 2
        actualStock = item[1];
        if (qty > actualStock):
            return 3
        self._update_buy(item[0], actualStock - qty)
        return 0

    def correct_error(self, nameup: str, qty: int = 1):
        """
        Corrects the quantity sold of an item.
        Args:
            nameup (str): The name of the item.
            qty (int): The quantity to subtract from the quantity sold. Default is 1.
        """
        item = self._get_row_by_name(nameup)
        if (not item):
            return 1
        if (qty <= 0):
            return 2
        actualStock = item[1];
        self._update_buy(item[0], actualStock + qty)
        return 0

    def refill_item(self, nameup: str, qty: int = 1):
        """
        An item has been sold qty time
        Args:
            nameup (str): The name of the item.
            qty (int): The quantity to add to the quantity sold. Default is 1.
        """
        item = self._get_row_by_name(nameup)
        if (not item):
            return 1
        if (qty < 0):
            return 2
        self._update_buy(item[0], qty)
        return 0

if __name__ == "__main__":
    print(rows)
