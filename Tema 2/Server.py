import http.server

from HttpHandler import HttpHandler
from Config import Config

PORT = Config().data["port"]
Handler = HttpHandler

with http.server.HTTPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
