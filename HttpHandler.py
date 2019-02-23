import json
import sys
from urllib import parse
from http.server import BaseHTTPRequestHandler

import requests

from Database import Database
from Log import Log
from config import Config


class HttpHandler(BaseHTTPRequestHandler):
    db = Database()
    config = Config().data

    def do_POST(self):
        if self.path == "/translate":
            data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            lang = ""
            if data.get("lang") is not None:
                lang = "en-" + data["lang"]
            text = ""
            if data.get("text") is not None:
                text = data["text"]
            r = requests.get("https://translate.yandex.net/api/v1.5/tr.json/translate",
                             params={"text": text, "lang": lang,
                                     "key": self.config["access_key"]})

            if r.status_code != 200:
                self.send_response(r.status_code)
                self.send_header('Content-type', 'text-html')
                self.end_headers()
                self.wfile.write(r.content)
                log = Log(r.elapsed.total_seconds(), r.content, 0, str({"text": text, "lang": lang}))
                self.db.insert_translation(log)
                return

            translated = ''.join(r.json()["text"])
            self.send_response(200)

            self.send_header('Content-type', 'text-html')
            self.end_headers()

            log = Log(r.elapsed.total_seconds(), r.content, 1, str({"text": text, "lang": lang}))
            self.db.insert_translation(log)

            self.wfile.write(translated.encode())

    def do_GET(self):
        args = {}
        idx = self.path.find('?')
        if idx >= 0:
            rpath = self.path[:idx]
            args = parse.parse_qs(self.path[idx + 1:])
        else:
            rpath = self.path
        # print(args)

        result = ""

        if rpath == '/se':
            uri = "https://api.stackexchange.com/2.2/questions"
            params = {"site": "stackoverflow", "pagesize": 1}
            if args.get("id") is not None:
                uri += '/' + args["id"][0]
            r = requests.get(uri, params=params)

            if r.status_code != 200:
                self.send_response(r.status_code)
                self.send_header('Content-type', 'text-html')
                self.end_headers()
                self.wfile.write(r.content)
                log = Log(r.elapsed.total_seconds(), r.content, 0, str({"site": "stackoverflow", "pagesize": 1}))
                self.db.insert_se(log)
                return

            result = r.json()
            if len(result["items"]) == 0:
                self.send_response(404)
                self.send_header('Content-type', 'text-html')
                self.end_headers()
                log = Log(r.elapsed.total_seconds(), r.content, 0, str({"site": "stackoverflow", "pagesize": 1}))
                self.db.insert_se(log)
                return

            title = result["items"][0]["title"]

            self.send_response(200)

            self.send_header('Content-type', 'text-html')
            self.end_headers()

            log = Log(r.elapsed.total_seconds(), r.content, 1, str({"site": "stackoverflow", "pagesize": 1}))
            self.db.insert_se(log)

            self.wfile.write(title.encode())
            return

        if rpath == '/random':
            min = 0
            max = 100000

            r = requests.get("https://qrng.anu.edu.au/API/jsonI.php", params={"length": 1, "type": "uint16"})

            try:
                if args.get("min") is not None:
                    min = int(args["min"][0])
                if args.get("max") is not None:
                    max = int(args["max"][0])

                if min > max:
                    raise ValueError("Min can not be bigger than max")

            except:
                self.send_response(400)
                self.send_header('Content-type', 'text-html')
                self.end_headers()
                self.wfile.write(str(sys.exc_info()[1]).encode())
                log = Log(r.elapsed.total_seconds(), r.content, 0, str({"length": 1, "type": "uint16"}))
                self.db.insert_random(log)
                return

            number = r.json()["data"][0]
            final = number % (max + 1 - min) + min

            # send code 200 response
            self.send_response(200)

            self.send_header('Content-type', 'text-html')
            self.end_headers()

            self.wfile.write(str(final).encode())

            log = Log(r.elapsed.total_seconds(), r.content, 1, str({"length": 1, "type": "uint16"}))
            self.db.insert_random(log)
            return

        if rpath == '/metrics':
            self.send_response(200)

            self.send_header('Content-type', 'text-html')
            self.end_headers()

            self.wfile.write(self.db.metrics().to_json().encode())

            return
