from Database import User, Repository
from Response import Response


class UserController:
    def __init__(self):
        self.repo = Repository(User)

    # GET ########################

    def get(self, id=None):
        if id is None:
            users = self.repo.get()
            return Response(True, users)

        user = self.repo.get(id)
        if user is None:
            return Response(False, "Not found", 404)
        return Response(True, user)

    def get_order(self, id, order_id=None):
        user = self.get(id)
        if not user.success:
            return user
        user = user.data
        if order_id is None:
            return Response(True, user.orders)
        order = list(filter(lambda o: o.id == int(order_id), user.orders))
        if len(order) == 0:
            return Response(False, "Not found", 404)
        return Response(True, order[0])

    def get_products(self, id, order_id, product_id=None):
        order = self.get_order(id, order_id)
        if not order.success:
            return order
        order = order.data
        if product_id is None:
            return Response(True, order.products)
        products = list(filter(lambda p: p.id == int(product_id), order.products))
        if len(products) == 0:
            return Response(False, "Not found", 404)
        return Response(True, products[0])

    # DELETE ########################
    def delete(self, id):
        user = self.repo.delete(id)
        if not user:
            return Response(False, "Not found", 404)
        return Response(True, '')
