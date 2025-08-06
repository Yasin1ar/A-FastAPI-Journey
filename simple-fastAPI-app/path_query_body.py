from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

class Item(BaseModel): # omitting this cause fastAPI to interpret item in route handlers as query params instead of req body
	name: str
	description: str | None = None
	price: float
	tax: float | None = None

# In-memory data store
items = [
	{"foo": {"name": "Foo", "price": 50.2}}, 
	{"bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2}}
]

# using query parameters for pagination. A practical, real world use of query params
@app.get("/items/")
async def get_items(skip: int = 0, limit: int = 10):
	items_to_return = items[skip: skip + limit]
	return {"items": items_to_return, "skip": skip, "limit": limit, "total": len(items)}

# using query param, body req, and path param all together
@app.post("/items/")
async def create_item(item_id: str, item: Item, q: str | None = None):
	result = {item_id: item.dict()}
	if q:
		result[item_id]['q'] = q  

	items.append(result)
	return JSONResponse(status_code=status.HTTP_201_CREATED, content=result)
