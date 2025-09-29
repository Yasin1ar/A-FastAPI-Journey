# Session-Based Authentication (FastAPI)

This module demonstrates session-based authentication in FastAPI using signed cookies with `fastapi-sessions`. It shows how to create sessions on login, attach them as cookies, read them on subsequent requests, and clear them on logout.

## 📁 Project Structure

```
authentication-techniques/session-based/
├── README.md              # This documentation file
└── main.py                # FastAPI app with cookie-based sessions
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- FastAPI[standard]
- fastapi-sessions

### Installation

```bash
pip install fastapi[standard] fastapi-sessions
```

## 📚 What This Module Covers

- Creating and storing session data on the server
- Issuing a signed session cookie to the client
- Reading session data on subsequent requests
- Logging out by deleting the session and cookie
- Using dependencies to gate-protect routes

## 🧩 How It Works

Key elements in `main.py`:

- Session data model (server-side):
  ```python
  class SessionData(BaseModel):
      username: str
  ```

- Frontend cookie (signed cookie issuer):
  ```python
  cookie = SessionCookie(
      cookie_name="session_id",
      identifier="general_verifier",
      auto_error=True,
      secret_key="my-super-secret-key-that-should-be-in-an-env-file",
      cookie_params=CookieParameters(),
  )
  ```

- Backend store (in-memory for demo):
  ```python
  backend = InMemoryBackend[uuid.UUID, SessionData]()
  ```

- Gatekeeper dependency (reads cookie and loads session):
  ```python
  async def get_session_data(session_id: uuid.UUID = Depends(cookie)):
      if session_id:
          session_data = await backend.read(session_id)
          if session_data:
              return session_data
      raise HTTPException(status_code=401, detail="Invalid or expired session")
  ```

- Login: create session, attach cookie, redirect to `/profile`:
  ```python
  @app.post("/login")
  async def login(username: str):
      session_id = uuid.uuid4()
      await backend.create(session_id, SessionData(username=username))
      response = RedirectResponse(url="/profile", status_code=303)
      cookie.attach_to_response(response, session_id)
      return response
  ```

- Logout: delete session and cookie, redirect to `/`:
  ```python
  @app.post("/logout")
  async def logout(session_id: uuid.UUID = Depends(cookie)):
      await backend.delete(session_id)
      response = RedirectResponse(url="/", status_code=303)
      cookie.delete_from_response(response)
      return response
  ```

- Protected route (recommended pattern):
  ```python
  @app.get("/profile")
  async def profile(session: SessionData = Depends(get_session_data)):
      return {"message": f"Welcome, {session.username}!"}
  ```

Note: The provided code returns a static profile response. To actually protect it, apply `Depends(get_session_data)` as shown above.

## ▶️ Running the App

```bash
# Development
fastapi dev main.py

# Or with Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🔐 API Usage

### Endpoints

| Method | Path            | Description                         |
|--------|-----------------|-------------------------------------|
| POST   | `/login`        | Creates a session, sets cookie      |
| GET    | `/profile`      | Example protected route             |
| POST   | `/logout`       | Deletes session and clears cookie   |

### Examples (curl)

Use a cookie jar to persist the `session_id` cookie between requests.

```bash
# 1) Login: creates a session and sets a cookie, redirects to /profile
curl -i -c jar.txt -X POST "http://localhost:8000/login?username=alice"

# 2) Access profile with the stored cookie
curl -b jar.txt http://localhost:8000/profile

# 3) Logout: deletes session and clears cookie
curl -i -b jar.txt -X POST http://localhost:8000/logout

# 4) Access profile again (should be 401 if protected with Depends(get_session_data))
curl -i -b jar.txt http://localhost:8000/profile
```

Example protected response:
```json
{"message": "Welcome, alice!"}
```

Example unauthorized response:
```json
{"detail": "Invalid or expired session"}
```

## 📖 Interactive Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🛡️ Security Notes

- Use a long, random `secret_key` and store it in environment variables.
- Use HTTPS in production so cookies are encrypted in transit.
- Mark cookies as `Secure`, `HttpOnly`, and set `SameSite` according to your needs.
- Use a persistent backend (e.g., Redis, database) in production instead of in-memory.

## 🎯 Learning Objectives

After this module, you should understand:

- ✅ How cookie-based sessions work in FastAPI
- ✅ How to create, attach, read, and delete sessions
- ✅ How to protect routes using a dependency
- ✅ How redirects and cookies interact during login/logout

## 🚀 Next Steps

- Switch to a persistent backend such as Redis
- Add real authentication (username/password verification)
- Implement session expiration and rotation
- Add CSRF protection for state-changing requests
- Integrate with frontend login forms and middleware