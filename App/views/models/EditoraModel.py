from App.dapendencias.config import Settings
from sqlalchemy import Integer, String, Column


class EditoraModel(Settings.DBBaseModel):
    __tablename__ = 'Editora'

    idEditora= Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256))
    endereco = Column(String(256))