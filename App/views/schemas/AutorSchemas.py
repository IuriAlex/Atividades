from typing import Optional

from pydantic import BaseModel


class EditoraSchemas(BaseModel):
    idAutor: Optional[int] = None
    nome: str
    nacionalidade: str

    class Config:
        orm_mode = True