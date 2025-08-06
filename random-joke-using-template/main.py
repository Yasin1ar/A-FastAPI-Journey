from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests as req

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/greet", response_class=HTMLResponse)
async def greet_and_joke(request: Request, name: str):
    # Fetch a random joke from the API
    response = req.get("https://official-joke-api.appspot.com/random_joke")
    joke = response.json()

    # Render the template with the name and joke
    return templates.TemplateResponse(
        "greeting.html", {"request": request, "name": name, "joke": joke}
    )
