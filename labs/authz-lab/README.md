# YASSINE / AuthZ Boundary Lab

Original fictional Python HTTP server with **three deliberately broken authorization boundaries**. Synthetic data only, no real targets, no outside network. Python 3.9+ standard library.

| Boundary | Vulnerable | Fixed |
|---|---|---|
| Account lifecycle | Accepts a demo token after account deletion | Rechecks account state on every request |
| Object authorization (BOLA) | Alice can read Bob's order | Owner or explicit admin permission required |
| Function authorization (BFLA) | Any signed-in member can create an admin invitation | Admin-only check |

## Run the lab

Terminal 1:

```bash
python3 server.py --mode vulnerable
```

Terminal 2:

```bash
# 1. BOLA: Alice asks for Bob's order.
curl -i -H 'Authorization: Bearer alice-demo-token' \
  http://127.0.0.1:8765/api/orders/4002

# 2. BFLA: Alice attempts an administrator-only action.
curl -i -X POST http://127.0.0.1:8765/api/admin/invitations \
  -H 'Authorization: Bearer alice-demo-token' \
  -H 'Content-Type: application/json' \
  --data '{"email":"candidate@lab.invalid"}'

# 3. Token remains effective after deleting Alice.
curl -i -X DELETE -H 'Authorization: Bearer alice-demo-token' \
  http://127.0.0.1:8765/api/me
curl -i -H 'Authorization: Bearer alice-demo-token' \
  http://127.0.0.1:8765/api/me
```

Stop terminal 1 with `Ctrl+C`, then run `python3 server.py --mode fixed` and replay the same requests. Expect **404**, **403**, and **401** respectively in fixed mode.

## Automated tests

```bash
python3 -m unittest -v test_lab.py
```

Two test scenarios assert vulnerable and fixed behavior using actual HTTP requests to automatically started localhost servers, including positive checks for legitimate access.

**Model limitations:** The tokens are intentionally unprotected demo strings. Real systems require signature and claim validation, expiry, revocation, consistent authorization policy enforcement, and tests for concurrency/CSRF where appropriate. A stale account token alone is not proof of remote account takeover without demonstrating an attacker can obtain and use it.
