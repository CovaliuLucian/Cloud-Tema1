from Database import Product, Repository
from Response import Response


class ProductController:
    def __init__(self):
        self.repo = Repository(Product)

    def get(self, id=None):
        if id is None:
            product = self.repo.get()
            return Response(True, product)

        product = self.repo.get(id)
        if product is None:
            return Response(False, "Not found", 404)
        return Response(True, product)

    def delete(self, id):
        if self.repo.delete(id):
            return Response(True, '')
        else:
            return Response(False, 'Not found', 404)

    def post(self, product, id=None):
        try:
            new_product = Product._from_json(product)
        except Exception as e:
            return Response(False, "Invalid data: " + str(e), 400)
        if id is not None:
            new_product.id = id
        try:
            self.repo.create(new_product)
        except Exception as e:
            print(str(e))
            return Response(False, "Conflict", 409)
        return Response(True, new_product)

    def put(self, product_data, id):
        product = self.get(id)
        if not product.success:
            return product
        old_product = product.data
        new_product = Product._from_json(product_data)
        old_product.name = new_product.name
        old_product.price = new_product.price
        self.repo.update()
        return Response(True, '')
