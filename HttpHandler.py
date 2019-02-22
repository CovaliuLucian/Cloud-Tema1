from http.server import BaseHTTPRequestHandler

import requests


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/test':
            r = requests.get("https://api.stackexchange.com/2.2/questions",
                             params={"site": "stackoverflow", "pagesize": 1})
            if r.status_code != 200:
                print(r.status_code)
                print(r.content)
                return

            title = r.json()["items"][0]["title"]

            r = requests.get("https://translate.yandex.net/api/v1.5/tr.json/translate",
                             params={"text": title, "lang": "en-ro",
                                     "key": "trnsl.1.1.20190222T104030Z.8db7db72bc8fb757.9573c1028bc38bb4e7688c6c3730c7df14be2e4a"})

            print(r.json())
            title = ''.join(r.json()["text"])

            r = requests.get("https://qrng.anu.edu.au/API/jsonI.php", params={"length": 1, "type": "uint8"})
            number = r.json()["data"][0]

            # send code 200 response
            self.send_response(200)

            # send header first
            self.send_header('Content-type', 'text-html')
            self.end_headers()

            # send file content to client
            self.wfile.write(title.encode())
            self.wfile.write(str(number).encode())
            return
