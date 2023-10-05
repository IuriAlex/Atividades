from typing import Optional

from pydantic import BaseModel, validator


class EstadoSchemas(BaseModel):
    idEmprestimo: Optional[int] = None
    idUsuario: int
    idObras: int
    idCategoria: int
    idEditora: int
    idEmprestimo: int
    dataEmprestimo: str
    dataEmprestimo: str
    status: str

    class Config:
        orm_mode = True
