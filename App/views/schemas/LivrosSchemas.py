from typing import Optional

from pydantic import BaseModel


class LivroSchemas(BaseModel):
    idObras: Optional[int] = None
    titulo: str
    classificacao: str
    lingua: str
    midia: str
    autorId: int
    editoraId: int
    categoriaId: int

    class Config:
        orm_mode = True