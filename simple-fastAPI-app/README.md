# FastAPI 101

This module covers the FastAPI basics including basic CRUD operations, the simplest possible FastAPI application, and practical demonstrations of path parameters, query parameters, and request body handling.

## 📁 Project Structure

```
simple-fastAPI-app/
├── README.md              # This documentation file
├── simplest_app.py        # Basic "Hello World" FastAPI application
├── path_query_body.py     # Demonstrates path, query, and body parameters
└── crud.py               # Complete CRUD operations with in-memory data store
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- FastAPI[standard]

### Installation

```bash
pip install fastapi[standard]
```

## 📚 File Descriptions

### 1. `simplest_app.py` - Hello World Example

The most basic FastAPI application demonstrating:
- FastAPI initialization
- Basic GET endpoint
- Return type annotations

**Run it:**
```bash
fastapi dev simplest_app.py
```

**Test it:**
```bash
curl http://localhost:8000/
# Response: {"message": "Hello World!"}
```

### 2. `path_query_body.py` - Parameter Handling

Demonstrates practical usage of:
- **Path Parameters**: Item ID in URL path
- **Query Parameters**: Pagination (`skip`, `limit`) and optional parameters (`q`)
- **Request Body**: Pydantic models for structured data
- **Status Codes**: Proper HTTP status code responses

**Features:**
- Pagination with `skip` and `limit` query parameters
- Item creation with path parameter, body, and optional query parameter
- Pydantic model validation
- JSON response with custom status codes

**Run it:**
```bash
fastapi dev path_query_body.py
```

**API Examples:**

```bash
# Get items with pagination
curl "http://localhost:8000/items/?skip=0&limit=2"

# Create item with path param, body, and query param
curl -X POST "http://localhost:8000/items/abc123?q=test" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item", "price": 29.99, "description": "A test item"}'
```

### 3. `crud.py` - Complete CRUD Operations

A comprehensive CRUD (Create, Read, Update, Delete) application featuring:
- **In-memory data store** with sample fruit items
- **Full CRUD operations** with proper error handling
- **Pagination and filtering** capabilities
- **HTTP status codes** and error responses
- **Pydantic models** for data validation

**Run it:**
```bash
fastapi dev crud.py
```

**API Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/items/` | Get all items with pagination and filtering |
| `GET` | `/items/{item_id}` | Get item by ID |
| `POST` | `/items/` | Create new item |
| `PUT` | `/items/{item_id}` | Update item by ID |
| `DELETE` | `/items/{item_id}` | Delete item by ID |

**Usage Examples:**

```bash
# Get all items
curl http://localhost:8000/items/

# Get items with pagination
curl "http://localhost:8000/items/?skip=0&limit=3"

# Filter items by name
curl "http://localhost:8000/items/?name=apple"

# Get specific item
curl http://localhost:8000/items/1

# Create new item
curl -X POST "http://localhost:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{"id": 11, "name": "Kiwi", "description": "Green kiwi fruit"}'

# Update item
curl -X PUT "http://localhost:8000/items/1" \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "name": "Red Apple", "description": "Fresh red apple"}'

# Delete item
curl -X DELETE http://localhost:8000/items/1
```

## 🔧 Key FastAPI Concepts Demonstrated

### 1. **Path Parameters**
```python
@app.get("/items/{item_id}")
def read_item(item_id: int) -> Item:
    # item_id is automatically converted to int
```

### 2. **Query Parameters**
```python
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    # Optional parameters with default values
```

### 3. **Request Body with Pydantic**
```python
class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

@app.post("/items/")
async def create_item(item: Item):
    # Automatic validation and type conversion
```

### 4. **Error Handling**
```python
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="Item not found")
```

### 5. **Status Codes**
```python
from fastapi import status
from fastapi.responses import JSONResponse

return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)
```

## 🎯 Learning Objectives

After completing this module, you'll understand:

- ✅ How to create a basic FastAPI application
- ✅ Path parameter handling and type conversion
- ✅ Query parameter usage for filtering and pagination
- ✅ Request body validation with Pydantic models
- ✅ Proper HTTP status codes and error handling
- ✅ Complete CRUD operations implementation
- ✅ API documentation with automatic OpenAPI/Swagger generation

## 📖 Interactive Documentation

FastAPI automatically generates interactive API documentation. After running any of the applications, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🚀 Next Steps

[check this out](../random-joke-using-template/README.md)