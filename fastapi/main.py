 from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI()
# uvicorn fastapi:app --reload

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item": item_id}


@app.post("/items/")
async def create_item(item: Item):
    return item


if __name__ == "__main__":
    print(root())
    print(get_item(10))