#!/usr/bin/env python3
"""HTTP regression tests for vulnerable and fixed modes using localhost only."""
import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from server import make_server


class TestLab(unittest.TestCase):
    def call(self, path, token=None, method='GET', data=None):
        headers = {}
        if token:
            headers['Authorization'] = 'Bearer ' + token
        if data is not None:
            headers['Content-Type'] = 'application/json'
        req = Request(self.base + path,
                      data=json.dumps(data).encode() if data is not None else None,
                      headers=headers, method=method)
        try:
            with urlopen(req, timeout=2) as response:
                return response.status, json.load(response)
        except HTTPError as err:
            return err.code, json.load(err)

    def exercise(self, mode):
        server = make_server(mode, 0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.base = 'http://127.0.0.1:%s' % server.server_port
        try:
            self.assertEqual(self.call('/api/orders/4002', 'alice-demo-token')[0],
                             200 if mode == 'vulnerable' else 404)
            self.assertEqual(self.call('/api/orders/4002', 'bob-demo-token')[0], 200)
            self.assertEqual(self.call('/api/admin/invitations', 'alice-demo-token', 'POST',
                                       {'email': 'demo@lab.invalid'})[0],
                             201 if mode == 'vulnerable' else 403)
            self.assertEqual(self.call('/api/admin/invitations', 'admin-demo-token', 'POST',
                                       {'email': 'new@lab.invalid'})[0], 201)
            self.assertEqual(self.call('/api/me', 'alice-demo-token', 'DELETE')[0], 200)
            self.assertEqual(self.call('/api/me', 'alice-demo-token')[0],
                             200 if mode == 'vulnerable' else 401)
            self.assertEqual(self.call('/api/me')[0], 401)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

    def test_vulnerable_outcomes(self):
        self.exercise('vulnerable')

    def test_fixed_guards(self):
        self.exercise('fixed')


if __name__ == '__main__':
    unittest.main(verbosity=2)
