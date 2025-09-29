from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext

app = FastAPI()
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user_from_db(username: str):
    # This is where you'd query your database for the user
    # For now, we'll use a fake dictionary
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
        # fake password to have a consistent response time. Good practice to avoid 'timing attack'
        password_to_check = "$2b$12$e6mGjCgX4oG5Fp7bC5vC4eA3jG5L6R7S8T9U0V1W2X3Y4Z5A6B9"
        
    verified_password = verify_password(credentials.password, password_to_check)
    if not user or not verified_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user

@app.get("/protected-route")
def protected_route(user: dict = Depends(authenticate_user)): # Depends is piece of code that do a specific job in FastAPI. More accurately, it is Dependency Injection 
    return {"message": f"Welcome, {user['username']}. You've made it past the bouncer."}