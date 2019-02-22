import http.server
import socketserver

from HttpHandler import HttpHandler

PORT = 55555
Handler = HttpHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()