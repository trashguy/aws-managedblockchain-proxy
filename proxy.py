import os

import requests
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from requests_auth_aws_sigv4 import AWSSigV4

PORT = os.getenv('PORT', 8086)
ENDPOINT = os.getenv('ENDPOINT')


def blockchainRequest(url_path, verb):
    x = AWSSigV4('managedblockchain')
    r_url = f'{ENDPOINT}/{url_path}'
    return requests.request(verb, r_url, auth=x)


class ProxyHTTPRequestHandler(SimpleHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'

    def do_HEAD(self):
        self.do_GET(body=False)
        return

    def do_GET(self, body=True):
        sent = False
        try:
            res = blockchainRequest(self.path[1:], 'GET')
            sent = True
            self.send_response(res.status_code)
            self.send_res_headers(res)
            msg = res.text
            if body:
                self.wfile.write(msg.encode(encoding='UTF-8', errors='strict'))
        finally:
            if not sent:
                self.send_error(404, 'error trying to proxy')

    def do_POST(self, body=True):
        sent = False
        try:
            res = blockchainRequest(self.path[1:], 'POST')
            sent = True
            self.send_response(res.status_code)
            self.send_res_headers(res)
            msg = res.text
            if body:
                self.wfile.write(msg.encode(encoding='UTF-8', errors='strict'))
        finally:
            if not sent:
                self.send_error(404, 'error trying to proxy')

    def parse_headers(self):
        req_header = {}
        for line in self.headers:
            line_parts = [o.strip() for o in line.split(':', 1)]
            if len(line_parts) == 2:
                req_header[line_parts[0]] = line_parts[1]
        return req_header

    def send_res_headers(self, res):
        res_headers = res.headers
        for key in res_headers:
            if key not in ['Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding', 'content-length', 'Content-Length']:
                self.send_header(key, res_headers[key])
        self.send_header('Content-Length', len(res.content))
        self.end_headers()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == '__main__':
    if not ENDPOINT:
        print('ENDPOINT needs to be set')
    try:
        with ThreadedHTTPServer(("", PORT), ProxyHTTPRequestHandler) as httpd:
            print(f'Server started listening on {PORT}')
            httpd.serve_forever()
    except KeyboardInterrupt:
        print('Shutting Down...')
