from App.dapendencias.config import Settings
from sqlalchemy import Integer, String, Column


class CategoriaModel(Settings.DBBaseModel):
    __tablename__ = 'Categoria'

    idCategoria = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(Integer)