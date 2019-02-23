import socketserver

from HttpHandler import HttpHandler
from config import Config

PORT = Config().data["port"]
Handler = HttpHandler

with socketserver.ThreadingTCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
