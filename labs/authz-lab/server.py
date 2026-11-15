#!/usr/bin/env python3
"""Original fictional localhost-only authorization lab, intentionally vulnerable."""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

TOKENS = {'alice-demo-token': 'alice', 'bob-demo-token': 'bob', 'admin-demo-token': 'admin'}


def make_server(mode='vulnerable', port=8765):
    if mode not in ('vulnerable', 'fixed'):
        raise ValueError('invalid mode')
    users = {
        'alice': {'role': 'member', 'deleted': False},
        'bob': {'role': 'member', 'deleted': False},
        'admin': {'role': 'admin', 'deleted': False},
    }
    orders = {
        '4001': {'owner': 'alice', 'item': 'Notebook', 'total': 42},
        '4002': {'owner': 'bob', 'item': 'Keyboard', 'total': 60},
    }
    invites = []

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass

        def reply(self, status, payload):
            raw = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def who(self):
            authorization = self.headers.get('Authorization', '')
            if not authorization.startswith('Bearer '):
                return None
            name = TOKENS.get(authorization[7:])
            if name is None or (mode == 'fixed' and users[name]['deleted']):
                return None
            return name

        def do_GET(self):
            path = urlsplit(self.path).path
            if path == '/health':
                return self.reply(200, {'lab': 'yassine-authz', 'mode': mode})
            name = self.who()
            if name is None:
                return self.reply(401, {'error': 'UNAUTHENTICATED'})
            if path == '/api/me':
                return self.reply(200, {'name': name, **users[name]})
            if path.startswith('/api/orders/'):
                order = orders.get(path.rsplit('/', 1)[-1])
                if order is None:
                    return self.reply(404, {'error': 'NOT_FOUND'})
                # Deliberate BOLA in vulnerable mode: no ownership check.
                if mode == 'fixed' and order['owner'] != name and users[name]['role'] != 'admin':
                    return self.reply(404, {'error': 'NOT_FOUND'})
                return self.reply(200, {'order': order})
            return self.reply(404, {'error': 'NOT_FOUND'})

        def do_DELETE(self):
            if urlsplit(self.path).path != '/api/me':
                return self.reply(404, {'error': 'NOT_FOUND'})
            name = self.who()
            if name is None:
                return self.reply(401, {'error': 'UNAUTHENTICATED'})
            users[name]['deleted'] = True
            return self.reply(200, {'deleted': name})

        def do_POST(self):
            if urlsplit(self.path).path != '/api/admin/invitations':
                return self.reply(404, {'error': 'NOT_FOUND'})
            name = self.who()
            if name is None:
                return self.reply(401, {'error': 'UNAUTHENTICATED'})
            # Deliberate BFLA: authenticated is not necessarily administrator.
            if mode == 'fixed' and users[name]['role'] != 'admin':
                return self.reply(403, {'error': 'FORBIDDEN'})
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if length < 1 or length > 4096:
                    raise ValueError('invalid body length')
                body = json.loads(self.rfile.read(length))
            except (ValueError, json.JSONDecodeError):
                return self.reply(400, {'error': 'INVALID_JSON'})
            if not isinstance(body, dict) or not isinstance(body.get('email'), str) or not body['email'].endswith('@lab.invalid'):
                return self.reply(400, {'error': 'INVALID_LAB_EMAIL'})
            invitation = {'id': len(invites) + 1, 'email': body['email'], 'role': 'admin', 'created_by': name}
            invites.append(invitation)
            return self.reply(201, {'invitation': invitation})

    return ThreadingHTTPServer(('127.0.0.1', port), Handler)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fictional local API trust-boundary lab')
    parser.add_argument('--mode', choices=('vulnerable', 'fixed'), default='vulnerable')
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    server = make_server(args.mode, args.port)
    print('Lab on http://127.0.0.1:%d [%s]' % (server.server_port, args.mode), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
