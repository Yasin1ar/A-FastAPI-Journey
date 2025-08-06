# Random Joke Generator with Templates

A simple FastAPI learning project that demonstrates template rendering with Jinja2 and external API integration. Fetches random jokes from an external API and displays them in a styled HTML page.

## Project Structure

```
random-joke-using-template/
├── README.md
├── main.py                # FastAPI application
└── templates/
    └── greeting.html      # Jinja2 template
```

## Setup

### Prerequisites
- Python 3.10+
- FastAPI[standard]
- Jinja2
- Requests

### Installation

```bash
cd random-joke-using-template
pip install fastapi[standard] jinja2 requests
```

## How It Works

The application demonstrates:
- Template rendering with Jinja2Templates
- External API integration using requests
- Query parameter handling
- HTML response generation

### Key Components

1. **External API**: Uses [Official Joke API](https://official-joke-api.appspot.com/random_joke) to fetch random jokes
2. **Template Rendering**: Jinja2 template with custom CSS styling
3. **Route Handler**: Single endpoint that accepts a name parameter and returns HTML

## Running the Application

```bash
# Development mode
fastapi dev main.py

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Usage

Visit the application with a name parameter:
```
http://localhost:8000/greet?name=YourName
```

### Example
```
http://localhost:8000/greet?name=Alice
```

This will display a personalized greeting with a random joke.


## Important Notes

- Must be in the `random-joke-using-template` directory to work
- Requires internet connection for joke API
- Each request fetches a new random joke

## Documentation

After starting the server:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Learning Objectives

This project covers:
- FastAPI template rendering
- External API integration
- Query parameter handling
- HTML response generation
- Basic web application structure

## Next Steps

[check this out](../authentication-techniques/README.md)