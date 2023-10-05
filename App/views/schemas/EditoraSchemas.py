from typing import Optional

from pydantic import BaseModel


class EmprestimoSchemas(BaseModel):
    idEditora: Optional[int] = None
    nome: str
    endereco: str

    class Config:
        orm_mode = True