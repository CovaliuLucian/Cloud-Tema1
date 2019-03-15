import sqlite3
from datetime import datetime

from Database import User, Repository, Order, Product
from Response import Response


class UserController:
    def __init__(self):
        self.repo = Repository(User)
        self.repo_orders = Repository(Order)
        self.repo_products = Repository(Product)

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

    # POST ########################

    def post(self, user, id=None):
        try:
            new_user = User._from_json(user)
        except Exception as e:
            return Response(False, "Invalid data: " + str(e), 400)
        if id is not None:
            new_user.id = id
        try:
            self.repo.create(new_user)
        except Exception as e:
            print(str(e))
            return Response(False, "Conflict", 409)
        return Response(True, new_user)

    def post_order(self, id, order, order_id=None):
        user = self.get(id)
        if not user.success:
            return user
        user = user.data
        try:
            new_order = Order._from_json(order)
        except Exception as e:
            return Response(False, "Invalid data: " + str(e), 400)
        place_date = datetime.strptime(new_order.place_date, "%Y-%m-%d").date()
        recv_date = datetime.strptime(new_order.recv_date, "%Y-%m-%d").date()
        if recv_date < place_date:
            return Response(False, "Unprocessable Entity", 422)
        if order_id is not None:
            new_order.id = order_id
        try:
            self.repo_orders.create(new_order)
        except Exception as e:
            print(str(e))
            return Response(False, "Conflict", 409)
        user.orders.append(new_order)
        self.repo.update()
        return Response(True, new_order)

    def post_product(self, id, order_id, product, product_id=None):
        order = self.get_order(id, order_id)
        if not order.success:
            return order
        order = order.data
        try:
            new_product = Product._from_json(product)
        except Exception as e:
            return Response(False, "Invalid data: " + str(e), 400)
        if product_id is not None:
            new_product.id = product_id
        try:
            self.repo_products.create(new_product)
        except Exception as e:
            print(str(e))
            return Response(False, "Conflict", 409)
        order.products.append(new_product)
        self.repo.update()
        return Response(True, new_product)

    # PUT ########################

    def put(self, user_data, id):
        user = self.get(id)
        if not user.success:
            return user
        old_user = user.data
        new_user = User._from_json(user_data)
        old_user.username = new_user.username
        old_user.address = new_user.address
        old_user.fullname = new_user.fullname
        self.repo.update()
        return Response(True, '')

    def put_order(self, id, order_data, order_id):
        order = self.get_order(id, order_id)
        if not order.success:
            return order
        old_order = order.data
        new_order = Order._from_json(order_data)
        old_order.recv_date = new_order.recv_date
        old_order.place_date = new_order.place_date
        old_order.cost = new_order.cost
        place_date = datetime.strptime(new_order.place_date, "%Y-%m-%d").date()
        recv_date = datetime.strptime(new_order.recv_date, "%Y-%m-%d").date()
        if recv_date < place_date:
            return Response(False, "Unprocessable Entity", 422)
        self.repo_orders.update()
        return Response(True, '')

    def put_product(self, id, order_id, product_data, product_id):
        product = self.get_products(id, order_id, product_id)
        if not product.success:
            return product
        old_product = product.data
        new_product = Product._from_json(product_data)
        old_product.name = new_product.name
        old_product.price = new_product.price
        self.repo_products.update()
        return Response(True, '')
