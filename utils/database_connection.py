import json

class DatabaseConnection:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.data = None

    def connect(self):
        try:
            with open(self.json_file_path, 'r') as json_file:
                self.data = json.load(json_file)
        except FileNotFoundError:
            self.data = None
            print("Error: json file not found.")

    def get_products(self):
        if self.data:
            return self.data.get('products', [])
        else:
            return []

    def add_product(self, new_product):
        if self.data:
            products = self.data.get('products', [])
            products.append(new_product)
            self.data['products'] = products
            with open(self.json_file_path, 'w') as json_file:
                json.dump(self.data, json_file, indent=4)
        else:
            print("Error: something went wrong adding the product")

    def get_categories(self):
        if self.data:
            return self.data.get('categories', [])
        else:
            return []

    def add_category(self, new_category):
        if self.data:
            categories = self.data.get('categories', [])
            categories.append(new_category)
            self.data['categories'] = categories
            with open(self.json_file_path, 'w') as json_file:
                json.dump(self.data, json_file, indent=4)
        else:
            print("Error: something went wrond adding category")

    def remove_category(self, category_name):
        if self.data:
            categories = self.data.get('categories', [])
            categories = [cat for cat in categories if cat["name"] != category_name] 
            self.data['categories'] = categories

            with open(self.json_file_path, 'w') as json_file:
                json.dump(self.data, json_file, indent=4)
        else:
            print("Error: something went wrond removing category")

    def get_favorites(self):
        if self.data:
            return self.data.get('favorites', [])
        else:
            return []

    def add_favorite(self, new_favorite):
        if self.data:
            favorites = self.data.get('favorites', [])
            favorites.append(new_favorite)
            self.data['favorites'] = favorites
            with open(self.json_file_path, 'w') as json_file:
                json.dump(self.data, json_file, indent=4)
        else:
            print("Error: something went wrong adding the favorite product")

    def get_items(self, key):
        """
        Obtiene una lista de elementos almacenados bajo una clave específica en el archivo JSON.
        """
        if self.data:
            return self.data.get(key, [])
        else:
            print("Error: Database not connected.")
            return []

    def add_item(self, key, new_item):
        """
        Agrega un nuevo elemento bajo una clave específica en el archivo JSON.
        """
        if self.data is not None:
            items = self.data.get(key, [])
            items.append(new_item)
            self.data[key] = items
            self._save_data()
        else:
            print("Error: Database not connected.")

    def remove_item(self, key, condition):
        """
        Elimina elementos bajo una clave específica que cumplan con una condición.
        """
        if self.data is not None:
            items = self.data.get(key, [])
            updated_items = [item for item in items if not condition(item)]
            self.data[key] = updated_items
            self._save_data()
        else:
            print("Error: Database not connected.")

    def _save_data(self):
        """
        Guarda los cambios realizados en la base de datos JSON.
        """
        try:
            with open(self.json_file_path, 'w') as json_file:
                json.dump(self.data, json_file, indent=4)
        except Exception as e:
            print(f"Error saving data to JSON file: {e}")
