#schemas.py
from pydantic import BaseModel
from typing import Optional

class ProductoBase(BaseModel):
    nombre: str
    precio: float
    stock: int

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None

class ProductoResponse(ProductoBase):
    id: int
    # Pydantic v2: usar from_attributes para ORM
    model_config = {"from_attributes": True}
        