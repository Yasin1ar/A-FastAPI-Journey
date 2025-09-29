## A FastAPI Journey

Hands-on examples exploring FastAPI fundamentals and common authentication patterns. Each folder is a self-contained mini-project you can run independently.

### What's inside
- `simple-fastAPI-app/`: Core FastAPI concepts (paths, query/body params, basic CRUD helpers).
- `random-joke-using-template/`: Server-side rendering with templates and a simple authenticated route.
- `authentication-techniques/`: Three auth approaches with runnable examples:
  - `basic-auth/` – HTTP Basic Auth with password hashing
  - `session-based/` – Cookie sessions backed by a server store
  - `jwt/` – OAuth2 password flow issuing JWT bearer tokens

### Prerequisites
- Python 3.10+
- Recommended: a virtual environment (e.g., `python -m venv .venv`)

### Getting started
Clone and enter the repository:
```bash
git clone https://github.com/<your-username>/A-FastAPI-Journey.git
cd A-FastAPI-Journey
```

Each example lists its own dependencies. Change into a module and install what it needs, then run the app.

#### Run: Simple FastAPI app
```bash
cd simple-fastAPI-app
pip install fastapi[standard]
fastapi dev simplest_app.py
# or
uvicorn simplest_app:app --reload --host 0.0.0.0 --port 8000
```

#### Run: Random joke with template
```bash
cd random-joke-using-template
pip install fastapi[standard]
fastapi dev main.py
```

#### Run: Authentication techniques
See the overview and detailed docs:
- `authentication-techniques/README.md`
- `authentication-techniques/basic-auth/README.md`
- `authentication-techniques/session-based/README.md`
- `authentication-techniques/jwt/README.md`

Quickstarts:
```bash
# Basic Auth
cd authentication-techniques/basic-auth
pip install fastapi[standard] passlib[bcrypt]
fastapi dev main.py

# Session-based
cd ../session-based
pip install fastapi[standard] fastapi-sessions
fastapi dev main.py

# JWT (token-based)
cd ../jwt
pip install fastapi[standard] passlib[bcrypt] PyJWT
fastapi dev main.py
```

### API docs
For any running app:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Repository structure
```
A-FastAPI-Journey/
├── authentication-techniques/
│   ├── basic-auth/
│   ├── session-based/
│   └── jwt/
├── random-joke-using-template/
├── simple-fastAPI-app/
└── LICENSE
```

### Security notes (high-level)
- Always use HTTPS in production.
- Store password hashes only (e.g., bcrypt), never plaintext.
- Keep secrets (session/JWT keys) in environment variables.
- For JWTs, use short expirations and consider refresh tokens.
- For sessions, mark cookies `Secure`, `HttpOnly`, and set `SameSite`.

### Contributing
Issues and PRs are welcome. If you add a new example, include a minimal `README.md` and clear run instructions.

### License
This project is licensed under the terms of the [LICENSE](LICENSE) file included in the repository.


