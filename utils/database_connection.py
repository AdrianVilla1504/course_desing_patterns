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




            

