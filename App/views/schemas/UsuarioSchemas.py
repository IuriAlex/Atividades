from typing import Optional

from pydantic import BaseModel


class UsuarioSchemas(BaseModel):
    idUsuario: Optional[int] = None
    nome: str
    endereco: str
    telefone: str
    cpf: int
    grupo: int

    class Config:
        orm_mode = True