import http.server
import socketserver

from HttpHandler import HttpHandler

PORT = 8080
Handler = HttpHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()