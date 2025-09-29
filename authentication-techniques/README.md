## Authentication Techniques in FastAPI

This directory contains three self‑contained FastAPI examples that demonstrate common authentication approaches. Each subfolder has its own `main.py` and README with details and runnable code.

### Modules
- [Basic Auth](./basic-auth/): Username/password checked on every request via `Authorization: Basic` header.
- [Session-Based](./session-based/): Server‑side sessions stored in a backend and tracked with a signed cookie.
- [JWT (Token-Based)](./jwt/): OAuth2 password flow issues bearer tokens (JWT) that clients send with requests.

### When to use which
- **Basic Auth**: Simple demos, internal tools over HTTPS, or as a temporary guard. No logout; credentials re-sent each request.
- **Session-Based**: Traditional web apps with server‑rendered pages or APIs closely tied to a browser. Easy server‑side invalidation.
- **JWT**: Stateless APIs and microservices. Good cross‑service auth; revocation/rotation policies needed.

### Quickstart
Prerequisites for all examples:
- Python 3.10+
- Install per module instructions below

Run commands from the module directory and use one of:
```bash
fastapi dev main.py
# or
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### Basic Auth
```bash
cd authentication-techniques/basic-auth
pip install fastapi[standard] passlib[bcrypt]
fastapi dev main.py
```
Test:
```bash
curl -u admin:secret-password http://localhost:8000/protected-route
```

#### Session-Based
```bash
cd authentication-techniques/session-based
pip install fastapi[standard] fastapi-sessions
fastapi dev main.py
```
Test (stores cookie in a jar file):
```bash
curl -i -c jar.txt -X POST "http://localhost:8000/login?username=alice"
curl -b jar.txt http://localhost:8000/profile
curl -i -b jar.txt -X POST http://localhost:8000/logout
```

#### JWT (Token-Based)
```bash
cd authentication-techniques/jwt
pip install fastapi[standard] passlib[bcrypt] PyJWT
fastapi dev main.py
```
Test:
```bash
TOKEN=$(curl -s -X POST -d "username=alice&password=wonderland" http://localhost:8000/token | jq -r .access_token)
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/profile
```

### Comparison
| Approach       | State lives | Client credential | Server invalidation | Best for |
|----------------|-------------|-------------------|---------------------|----------|
| Basic Auth     | None        | Password each req | N/A                 | Very simple demos/tools |
| Session-Based  | Server      | Signed cookie     | Easy (delete/expire)| Browser‑centric apps |
| JWT (Bearer)   | Client      | JWT access token  | Harder (needs lists/rotation) | Public APIs, microservices |

### Security notes
- Always use HTTPS in production.
- Store only password hashes (e.g., bcrypt), never plaintext.
- Keep secrets (session keys, JWT keys) in environment variables.
- For JWTs, use short expirations and consider refresh tokens + rotation.
- For sessions, mark cookies as `Secure`, `HttpOnly`, and set `SameSite`.

### Directory structure
```
authentication-techniques/
├── basic-auth/
│   ├── README.md
│   └── main.py
├── session-based/
│   ├── README.md
│   └── main.py
└── jwt/
    ├── README.md
    └── main.py
```

Refer to each module’s README for deeper explanations, code snippets, and extended examples.