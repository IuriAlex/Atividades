from typing import Optional

from pydantic import BaseModel


class CategoriaSchemas(BaseModel):
    idCategoria: Optional[int] = None
    nome: str

    class Config:
        orm_mode = True