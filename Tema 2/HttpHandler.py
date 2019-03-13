import json
import re
from http.server import BaseHTTPRequestHandler

from Config import Config
from Util import Utilities
from Database import Repository, User
from UserController import UserController
from ProductController import ProductController
from Response import Response


class HttpHandler(BaseHTTPRequestHandler):
    user_controller = UserController()
    product_controller = ProductController()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST, PUT, PATCH, DELETE')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        rpath, args = Utilities.get_args(self.path)
        resp = Response(False, "Not found", 404)
        components = rpath.split("/")
        components = list(filter(lambda a: a != "", components))
        if components[0] == "users":
            if len(components) == 1:
                resp = self.user_controller.get()
            if len(components) == 2:
                resp = self.user_controller.get(components[1])
            if len(components) > 2 and components[2] == "orders":
                user_id = components[1]
                if len(components) == 3:
                    resp = self.user_controller.get_order(user_id)
                if len(components) == 4:
                    resp = self.user_controller.get_order(user_id, components[3])
                if len(components) > 4 and components[4] == "products":
                    order_id = components[3]
                    if len(components) == 5:
                        resp = self.user_controller.get_products(user_id, order_id)
                    if len(components) == 6:
                        resp = self.user_controller.get_products(user_id, order_id, components[5])

        if components[0] == "products":
            if len(components) == 1:
                resp = self.product_controller.get()
            if len(components) == 2:
                resp = self.product_controller.get(components[1])

        print(resp.to_json())

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(resp.to_json())
        return
