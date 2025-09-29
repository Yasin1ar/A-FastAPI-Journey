import uuid
from typing import Dict, Union
from fastapi import FastAPI, HTTPException, status, Depends
from starlette.responses import RedirectResponse
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from pydantic import BaseModel

app = FastAPI()


# 1. The Session Data Model
# This is what we'll store on the server side. Keep it simple.
class SessionData(BaseModel):
    username: str


# 2. The Frontend (The Cookie)
# This handles the creation and deletion of the cookie.
# The 'secret_key' is critical. This should be a long, random string in production.
cookie_params = CookieParameters()
cookie = SessionCookie(
    cookie_name="session_id",
    identifier="general_verifier",
    auto_error=True,
    secret_key="my-super-secret-key-that-should-be-in-an-env-file",
    cookie_params=cookie_params,
)

# 3. The Backend (The Server's Memory)
# This is where the session data lives.
# In production, use a persistent store like Redis or a database.
# In-memory is great for a simple example, but your data will vanish if the server restarts.
backend = InMemoryBackend[uuid.UUID, SessionData]()


# 4. The "Gatekeeper" Dependency
# This is a special function that checks the session for us.
# It reads the cookie and fetches the data from the backend.
async def get_session_data(session_id: uuid.UUID = Depends(cookie)):
    if session_id:
        session_data = await backend.read(session_id)
        if session_data:
            return session_data
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired session",
    )


@app.post("/login")
async def login(username: str):
    # In a real app, you would verify the username/password here.
    # For this example, we'll just assume they're valid.

    session_id = uuid.uuid4()
    session_data = SessionData(username=username)
    await backend.create(session_id, session_data)

    response = RedirectResponse(url="/profile", status_code=status.HTTP_303_SEE_OTHER)
    cookie.attach_to_response(response, session_id)
    return response


@app.post("/logout")
async def logout(session_id: uuid.UUID = Depends(cookie)):
    await backend.delete(session_id)
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    cookie.delete_from_response(response)
    return response


@app.get("/profile")
async def profile():
    return {"message": "Hey! welcome to your dashboard!"}
