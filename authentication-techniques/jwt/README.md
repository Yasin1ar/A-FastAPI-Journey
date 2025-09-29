# JWT (Token-Based Authentication) with FastAPI

This module demonstrates token-based authentication using JSON Web Tokens (JWT) in FastAPI. It covers issuing tokens via the OAuth2 password flow, verifying tokens on protected routes, handling expiration, and common security considerations.

## 📁 Project Structure

```
authentication-techniques/jwt/
├── README.md              # This documentation file
└── main.py                # FastAPI app with JWT auth
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- fastapi[standard]
- passlib[bcrypt]
- PyJWT (jwt)

### Installation

```bash
pip install fastapi[standard] passlib[bcrypt] PyJWT
```

## 📚 What This Module Covers

- OAuth2 password flow with `/token` endpoint
- Password hashing and verification using `passlib`
- Creating JWT access tokens with expiration
- Protecting routes using `OAuth2PasswordBearer`
- Decoding and validating JWTs (signature, expiration, subject)

## 🧩 How It Works

Key elements in `main.py`:

- Token creation
  ```python
  def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
      to_encode = data.copy()
      expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=30))
      to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
      encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
      return encoded_jwt
  ```

- OAuth2 token endpoint
  ```python
  @app.post("/token", response_model=Token)
  async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
      user = authenticate_user(form_data.username, form_data.password)
      if not user:
          raise HTTPException(status_code=401, detail="Incorrect username or password")
      access_token = create_access_token(data={"sub": user.username})
      return {"access_token": access_token, "token_type": "bearer"}
  ```

- Protected route and token verification
  ```python
  oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

  async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
      token_data = decode_token(token)
      user = get_user(token_data.username) if token_data.username else None
      if user is None:
          raise HTTPException(status_code=401, detail="User not found")
      return user
  ```

## ▶️ Running the App

```bash
# Development
fastapi dev main.py

# Or with Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🔐 API Usage

### Get Token

- Method: `POST`
- Path: `/token`
- Body (x-www-form-urlencoded): `username`, `password`

Example:
```bash
curl -X POST -d "username=alice&password=wonderland" http://localhost:8000/token
```
Response:
```json
{"access_token": "<JWT>", "token_type": "bearer"}
```

### Access Protected Route

- Method: `GET`
- Path: `/profile`
- Header: `Authorization: Bearer <JWT>`

Example:
```bash
TOKEN=$(curl -s -X POST -d "username=alice&password=wonderland" http://localhost:8000/token | jq -r .access_token)
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/profile
```

Example response:
```json
{"username": "alice", "full_name": "Alice Anderson"}
```

### Health Check
```bash
curl http://localhost:8000/health
```

## 📖 Interactive Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🛡️ Security Notes

- Use a long, random `JWT_SECRET_KEY` from environment variables.
- Set short expiration times and rotate tokens when needed.
- Prefer HTTPS to protect tokens in transit.
- Consider refresh tokens for longer sessions.
- Scope tokens (add claims like roles/permissions) as needed.

## 🎯 Learning Objectives

After this module, you should understand:

- ✅ How to implement OAuth2 password authentication with JWT
- ✅ How to generate, sign, and validate JWTs
- ✅ How to secure endpoints with bearer tokens
- ✅ Best practices around token security

## 🚀 Next Steps

- Add refresh tokens and token rotation
- Persist users in a real database
- Add role/permission claims and enforce authorization
- Move secrets to environment and configure CORS

