class ProductFilter:
    def filter(self, products, **kwargs):
        raise NotImplementedError

class CategoryFilter(ProductFilter):
    def filter(self, products, category):
        return [p for p in products if p['category'].lower() == category.lower()]

class IDFilter(ProductFilter):
    def filter(self, products, product_id):
        return next((p for p in products if p['id'] == product_id), None)