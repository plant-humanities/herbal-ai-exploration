#!/usr/bin/env python
# -*- coding: utf-8 -*-

from http.server import HTTPServer, SimpleHTTPRequestHandler
import argparse, os, re

args = argparse.ArgumentParser(description='Juncture dev server')
args.add_argument('--localifc', default=False, action='store_true', help='Use local IFC server')
args.add_argument('--ifcroot', default='../../rsnyder/ifc', help='Path to local IFC code')
args = vars(args.parse_args())
use_localifc = args['localifc']
ifc_root = args['ifcroot']

index_html = open('./dev/index.html', 'rb').read()
if use_localifc:
    index_html = re.sub(b'https://ifc.juncture-digital.org', b'', index_html)

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    
    def return_content(self, content=index_html, mime='text/html', status=200):
        self.send_response(status)
        self.send_header('Content-Type', mime)
        self.end_headers()
        return self.wfile.write(content)

    def do_GET(self):
        if self.path.split('/')[1] in ('js', 'css'):
            return self.return_content(open(f'{ifc_root}{self.path}', 'rb').read(), mime='text/javascript' if self.path.endswith('.js') else 'text/css')
        if self.path == '/':
            return self.return_content()
        elif os.path.isdir(f'.{self.path}'):
            return self.return_content(status=404)
        else:
            return super().do_GET()
            
    def send_error(self, code, message=None, explain=None):
        if code == 404:
            print (f"404: {self.path}")
            return self.return_content(status=404)
        else:
            super().send_error(code, message, explain)

if __name__ == "__main__":
    port = 8888
    server = HTTPServer(('localhost', port), CustomHTTPRequestHandler)
    print(f"Serving on port {port}...")
    server.serve_forever()