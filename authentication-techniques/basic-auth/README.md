# Basic HTTP Authentication (FastAPI)

This module demonstrates Basic Authentication in FastAPI using `HTTPBasic` and password hashing with `passlib[bcrypt]`. It shows how to protect endpoints, validate credentials, and return proper HTTP responses.

## 📁 Project Structure

```
authentication-techniques/basic-auth/
├── README.md              # This documentation file
└── main.py                # FastAPI app with Basic Auth
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- FastAPI[standard]
- passlib[bcrypt]

### Installation

```bash
pip install fastapi[standard] passlib[bcrypt]
```

## 📚 What This Module Covers

- Using `HTTPBasic` to read credentials from the `Authorization: Basic` header
- Hashing and verifying passwords with `passlib` (bcrypt)
- Protecting endpoints with dependencies (`Depends`)
- Returning correct status codes and headers for unauthorized requests
- Mitigating timing attacks by using a constant-time code path

## 🧩 How It Works

Key elements in `main.py`:

- Security scheme:
  ```python
  from fastapi.security import HTTPBasic
  security = HTTPBasic()
  ```

- Password hashing and verification:
  ```python
  from passlib.context import CryptContext
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

  def verify_password(plain_password, hashed_password) -> bool:
      return pwd_context.verify(plain_password, hashed_password)
  ```

- Fake user store (demo only) and authentication dependency:
  ```python
  def get_user_from_db(username: str):
      fake_users_db = {
          "admin": {
              "username": "admin",
              "hashed_password": pwd_context.hash("secret-password")
          }
      }
      return fake_users_db.get(username)

  def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
      user = get_user_from_db(credentials.username)
      if user:
          password_to_check = user["hashed_password"]
      else:
          # constant-time verification path to mitigate timing attacks
          password_to_check = "$2b$12$e6mGjCgX4oG5Fp7bC5vC4eA3jG5L6R7S8T9U0V1W2X3Y4Z5A6B9"

      verified_password = verify_password(credentials.password, password_to_check)
      if not user or not verified_password:
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Incorrect username or password",
              headers={"WWW-Authenticate": "Basic"},
          )
      return user
  ```

- Protected endpoint:
  ```python
  @app.get("/protected-route")
  def protected_route(user: dict = Depends(authenticate_user)):
      return {"message": f"Welcome, {user['username']}. You've made it past the bouncer."}
  ```

## ▶️ Running the App

```bash
# Development
fastapi dev main.py

# Or with Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🔐 API Usage

### Endpoint

- Method: `GET`
- Path: `/protected-route`
- Security: Basic Auth (username/password via `Authorization: Basic` header)

### Examples (curl)

```bash
# Correct credentials (admin / secret-password)
curl -u admin:secret-password http://localhost:8000/protected-route

# Incorrect credentials (401 Unauthorized)
curl -u admin:wrong http://localhost:8000/protected-route

# Without credentials (401 with WWW-Authenticate header)
curl -i http://localhost:8000/protected-route | sed -n '1,10p'
```

Example success response:
```json
{"message": "Welcome, admin. You've made it past the bouncer."}
```

Example error response:
```json
{"detail": "Incorrect username or password"}
```

The error includes `WWW-Authenticate: Basic`, which prompts browsers to show a login dialog.

## 📖 Interactive Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🛡️ Security Notes

- Use HTTPS in production so credentials are encrypted in transit.
- Do not store plaintext passwords. Store only strong hashes (e.g., bcrypt).
- Replace the demo user store with a real database.
- Keep authentication logic constant-time to reduce timing side channels.

## 🎯 Learning Objectives

After this module, you should understand:

- ✅ How Basic Auth works in FastAPI (`HTTPBasic`)
- ✅ How to hash and verify passwords with `passlib`
- ✅ How to protect routes using dependencies
- ✅ Proper HTTP responses and headers for authentication

## 🚀 Next Steps

- Persist users in a database and manage migrations
- Add registration, password reset, and account lockout policies
- Integrate rate limiting and logging
- Explore session-based or token-based auth (see `authentication-techniques/session-based/`)