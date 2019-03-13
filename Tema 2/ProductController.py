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
