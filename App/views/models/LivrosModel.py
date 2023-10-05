from App.dapendencias.config import Settings
from sqlalchemy import Integer, String, Column


class LivrosModel(Settings.DBBaseModel):
    __tablename__ = 'Livros'

    idObras = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(256))
    classificacao = Column(String(256))
    lingua = Column(String(256))
    midia = Column(String(256))
    autorId = Column(Integer)
    editoraId = Column(Integer)
    categoriaId = Column(Integer)
