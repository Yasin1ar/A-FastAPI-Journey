from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# In-memory data store
items = [
    Item(id=1, name="Apple", description="Fresh red apple"),
    Item(id=2, name="Banana", description="Ripe yellow banana"),
    Item(id=3, name="Orange", description="Juicy orange fruit"),
    Item(id=4, name="Grapes", description="Seedless green grapes"),
    Item(id=5, name="Mango", description="Sweet mango fruit"),
    Item(id=6, name="Blueberry", description="Small blue berries"),
    Item(id=7, name="Strawberry", description="Red ripe strawberries"),
    Item(id=8, name="Pineapple", description="Tropical fruit with spiky skin"),
    Item(id=9, name="Watermelon", description="Large green watermelon"),
    Item(id=10, name="Lemon", description="Sour yellow lemon")
]

# Create an item
@app.post("/items/")
def create_item(item: Item) -> Item:
    if any(existing_item.id == item.id for existing_item in items):
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items.append(item)
    return item

# Read all items with optional filtering and pagination
@app.get("/items/")
def read_items(
    skip: int = 0,
    limit: int = 10,
    name_filter: Optional[str] = Query(None, alias="name")
) -> List[Item]:
    # Filter by name if filter is provided
    filtered_items = items
    if name_filter:
        filtered_items = [item for item in items if name_filter.lower() in item.name.lower()]
    
    # Pagination by skipping and limiting
    return filtered_items[skip: skip + limit]

# Read a single item by ID
@app.get("/items/{item_id}")
def read_item(item_id: int) ->  Item:
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# Update an item by ID
@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: Item) -> Item:
    for index, item in enumerate(items):
        if item.id == item_id:
            items[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# Delete an item by ID
@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int) -> None:
    for index, item in enumerate(items):
        if item.id == item_id:
            del items[index]
            return
    raise HTTPException(status_code=404, detail="Item not found")
