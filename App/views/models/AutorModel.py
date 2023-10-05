from App.dapendencias.config import Settings
from sqlalchemy import Integer, String, Column


class AutorModel(Settings.DBBaseModel):
    __tablename__ = 'Autor'

    idAutor = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256))
    nacionalidade = Column(String(256))