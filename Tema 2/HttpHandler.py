import json
import re
from http.server import BaseHTTPRequestHandler

from Config import Config
from Util import Utilities
from Database import Repository, User
from UserController import UserController
from ProductController import ProductController
from Response import Response
from OrderController import OrderController


class HttpHandler(BaseHTTPRequestHandler):
    user_controller = UserController()
    product_controller = ProductController()
    order_controller = OrderController()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST, PUT, PATCH, DELETE')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        try:
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

            if components[0] == "serverulfacultatii":
                resp = Response(False, "Service Unavailable", 503)

            if components[0] == "licenta":
                resp = Response(False, "Not Implemented", 501)

            print(resp.to_json())

            if not resp.success:
                self.send_response(resp.error)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(resp.data.encode())
                return

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(resp.to_json())
            return
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(str(e).encode())
            return

    def do_DELETE(self):
        try:
            rpath, args = Utilities.get_args(self.path)
            resp = Response(False, "Not found", 404)
            components = rpath.split("/")
            components = list(filter(lambda a: a != "", components))
            if components[0] == "users":
                if len(components) == 1:
                    resp = Response(False, "Method not allowed", 405)
                if len(components) == 2:
                    resp = self.user_controller.delete(components[1])
                if len(components) > 2 and components[2] == "orders":
                    user_id = components[1]
                    if len(components) == 3:
                        resp = Response(False, "Method not allowed", 405)
                    if len(components) == 4:
                        order = self.user_controller.get_order(user_id, components[3])
                        if order.success:
                            resp = self.order_controller.delete(components[3])
                        else:
                            resp = order
                    if len(components) > 4 and components[4] == "products":
                        order_id = components[3]
                        if len(components) == 5:
                            resp = Response(False, "Method not allowed", 405)
                        if len(components) == 6:
                            product = self.user_controller.get_products(user_id, order_id, components[5])
                            if product.success:
                                resp = self.product_controller.delete(components[5])
                            else:
                                resp = product

            if components[0] == "products":
                if len(components) == 1:
                    resp = Response(False, "Method not allowed", 405)
                if len(components) == 2:
                    resp = self.product_controller.delete(components[1])

            print(resp.to_json())

            if not resp.success:
                self.send_response(resp.error)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(resp.data.encode())
                return

            self.send_response(204)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # self.wfile.write(resp.to_json())
            return
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(str(e).encode())
            return

    def do_POST(self):
        try:
            rpath, args = Utilities.get_args(self.path)
            resp = Response(False, "Not found", 404)

            components = rpath.split("/")
            components = list(filter(lambda a: a != "", components))

            try:
                data = json.loads(self.rfile.read(int(self.headers['content-length'])).decode())
            except Exception as e:
                resp = Response(False, "Invalid data: " + str(e), 400)
                components[0] = ''  # don't @me

            if components[0] == "users":
                if len(components) == 1:
                    resp = self.user_controller.post(data)
                if len(components) == 2:
                    resp = self.user_controller.post(data, components[1])
                if len(components) > 2 and components[2] == "orders":
                    user_id = components[1]
                    if len(components) == 3:
                        resp = self.user_controller.post_order(user_id, data)
                    if len(components) == 4:
                        resp = self.user_controller.post_order(user_id, data, components[3])
                    if len(components) > 4 and components[4] == "products":
                        order_id = components[3]
                        if len(components) == 5:
                            resp = self.user_controller.post_product(user_id, order_id, data)
                        if len(components) == 6:
                            resp = self.user_controller.post_product(user_id, order_id, data, components[5])

            if components[0] == "products":
                if len(components) == 1:
                    resp = self.product_controller.post(data)
                if len(components) == 2:
                    resp = self.product_controller.post(data, components[1])

            print(resp.to_json())

            if not resp.success:
                self.send_response(resp.error)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(resp.data.encode())
                return

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(resp.to_json())
            return
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(str(e).encode())
            return

    def do_PUT(self):
        try:
            rpath, args = Utilities.get_args(self.path)
            resp = Response(False, "Not found", 404)

            components = rpath.split("/")
            components = list(filter(lambda a: a != "", components))

            try:
                data = json.loads(self.rfile.read(int(self.headers['content-length'])).decode())
            except Exception as e:
                resp = Response(False, "Invalid data: " + str(e), 400)
                components[0] = ''  # don't @me

            if components[0] == "users":
                if len(components) == 1:
                    resp = Response(False, "Method not allowed", 405)
                if len(components) == 2:
                    resp = self.user_controller.put(data, components[1])
                if len(components) > 2 and components[2] == "orders":
                    user_id = components[1]
                    if len(components) == 3:
                        resp = Response(False, "Method not allowed", 405)
                    if len(components) == 4:
                        resp = self.user_controller.put_order(user_id, data, components[3])
                    if len(components) > 4 and components[4] == "products":
                        order_id = components[3]
                        if len(components) == 5:
                            resp = Response(False, "Method not allowed", 405)
                        if len(components) == 6:
                            resp = self.user_controller.put_product(user_id, order_id, data, components[5])

            if components[0] == "products":
                if len(components) == 1:
                    resp = Response(False, "Method not allowed", 405)
                if len(components) == 2:
                    resp = self.product_controller.put(data, components[1])

            print(resp.to_json())

            if not resp.success:
                self.send_response(resp.error)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(resp.data.encode())
                return

            self.send_response(204)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # self.wfile.write(resp.to_json())
            return
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(str(e).encode())
            return
