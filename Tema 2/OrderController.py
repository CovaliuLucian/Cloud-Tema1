from Database import Order, Repository
from Response import Response


class OrderController:
    def __init__(self):
        self.repo = Repository(Order)

    def delete(self, id):
        if self.repo.delete(id):
            return Response(True, '')
        else:
            return Response(False, 'Not found', 404)
