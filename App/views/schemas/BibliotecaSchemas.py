from typing import Optional

from pydantic import BaseModel


class CategoriaSchemas(BaseModel):
    codigo: Optional[int] = None
    idUsuario: int
    idObras: int

    class Config:
        orm_mode = True