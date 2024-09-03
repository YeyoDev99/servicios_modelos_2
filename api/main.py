from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

app = FastAPI()

items_db = {}

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.get("/")
def home_page():
    return {"message": "welcome to the homepage Simar (that's right we speak gringo)."}



@app.get("/items")
def read_items():
    """Retrieve a list of all items."""
    if not items_db:
        return {"message": "No items available"}
    return {"items": list(items_db.values())}

@app.post("/items")
def create_item(item: Item):
    """Create a new item."""
    item_id = len(items_db) + 1 
    items_db[item_id] = item.dict()
    return {"message": "Item created", "item": items_db[item_id]}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    """Retrieve a single item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items_db[item_id]}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """Update an existing item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item.dict()
    return {"message": f"Item {item_id} updated", "item": items_db[item_id]}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """Delete an item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": f"Item {item_id} deleted"}

@app.patch("/items/{item_id}")
def patch_item(item_id: int, item: Item):
    """Partially update an item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    stored_item_data = items_db[item_id]
    update_data = item.dict(exclude_unset=True)
    stored_item_data.update(update_data)
    items_db[item_id] = stored_item_data
    return {"message": f"Item {item_id} partially updated", "item": items_db[item_id]}

@app.trace("/items/{item_id}")
async def trace_item(item_id: int, request: Request):
    """Trace request details for an item."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {
        "method": request.method,
        "headers": dict(request.headers),
        "body": await request.body()
    }
