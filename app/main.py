from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="GitHub Actions Learning API",
    description="Uma API para aprender GitHub Actions com FastAPI",
    version="1.0.0"
)

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

# Banco de dados em memória para exemplo
fake_db = [
    Item(id=1, name="Item 1", description="Descrição do item 1", price=9.99),
    Item(id=2, name="Item 2", description="Descrição do item 2", price=19.99),
]

@app.get("/")
async def read_root():
    return {"message": "GitHub Actions modified this 2!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/items", response_model=List[Item])
async def read_items():
    return fake_db

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    item = next((item for item in fake_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    if any(existing_item.id == item.id for existing_item in fake_db):
        raise HTTPException(status_code=400, detail="Item já existe")
    fake_db.append(item)
    return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)