#!/usr/bin/env python3
"""Admin API for Sign Of Times — port 8084"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os, uuid

WATCHES_FILE = '/var/www/steeve/watches.json'
CONTENT_FILE = '/var/www/steeve/site_content.json'
IMAGES_DIR   = '/var/www/steeve/images/'
ADMIN_PASS   = 'signoftimes2026'

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def send_json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.end_headers()

    def check_auth(self):
        return self.headers.get('Authorization','') == f'Bearer {ADMIN_PASS}'

    def read_json(self, path):
        with open(path, encoding='utf-8') as f:
            return json.load(f)

    def write_json(self, path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def body(self):
        length = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(length))

    # ── GET ──────────────────────────────────────────────────
    def do_GET(self):
        if self.path == '/api/watches':
            self.send_json(200, self.read_json(WATCHES_FILE))
        elif self.path == '/api/content':
            self.send_json(200, self.read_json(CONTENT_FILE))
        else:
            self.send_json(404, {'error': 'not found'})

    # ── POST ─────────────────────────────────────────────────
    def do_POST(self):
        if not self.check_auth():
            return self.send_json(401, {'error': 'unauthorized'})

        if self.path == '/api/watches':
            data = self.body()
            watches = self.read_json(WATCHES_FILE)
            data['id'] = max((w['id'] for w in watches), default=-1) + 1
            data.setdefault('sold', False)
            watches.append(data)
            self.write_json(WATCHES_FILE, watches)
            self.send_json(201, data)

        elif self.path == '/api/upload':
            length = int(self.headers.get('Content-Length', 0))
            raw = self.rfile.read(length)
            ct = self.headers.get('content-type', '')
            boundary = ct.split('boundary=')[-1].encode()
            for part in raw.split(b'--' + boundary):
                if b'filename=' in part:
                    header, _, body = part.partition(b'\r\n\r\n')
                    fname_raw = header.split(b'filename="')[1].split(b'"')[0].decode()
                    ext = os.path.splitext(fname_raw)[1].lower() or '.jpg'
                    fname = f'watch_{uuid.uuid4().hex[:8]}{ext}'
                    with open(os.path.join(IMAGES_DIR, fname), 'wb') as out:
                        out.write(body.rstrip(b'\r\n'))
                    return self.send_json(200, {'filename': fname})
            self.send_json(400, {'error': 'no file'})

        else:
            self.send_json(404, {'error': 'not found'})

    # ── PUT ──────────────────────────────────────────────────
    def do_PUT(self):
        if not self.check_auth():
            return self.send_json(401, {'error': 'unauthorized'})

        parts = self.path.split('/')
        if self.path == '/api/content':
            data = self.body()
            self.write_json(CONTENT_FILE, data)
            self.send_json(200, {'ok': True})
        elif len(parts) == 4 and parts[2] == 'watches':
            wid = int(parts[3])
            data = self.body()
            watches = self.read_json(WATCHES_FILE)
            for i, w in enumerate(watches):
                if w['id'] == wid:
                    watches[i].update(data)
                    break
            self.write_json(WATCHES_FILE, watches)
            self.send_json(200, {'ok': True})
        else:
            self.send_json(404, {'error': 'not found'})

    # ── DELETE ───────────────────────────────────────────────
    def do_DELETE(self):
        if not self.check_auth():
            return self.send_json(401, {'error': 'unauthorized'})
        parts = self.path.split('/')
        if len(parts) == 4 and parts[2] == 'watches':
            wid = int(parts[3])
            watches = [w for w in self.read_json(WATCHES_FILE) if w['id'] != wid]
            self.write_json(WATCHES_FILE, watches)
            self.send_json(200, {'ok': True})
        else:
            self.send_json(404, {'error': 'not found'})

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8084), Handler)
    print('Sign Of Times Admin API — port 8084')
    server.serve_forever()
