from App.dapendencias.config import Settings
from sqlalchemy import Integer, String, Column


class BibliotecaModel(Settings.DBBaseModel):
    __tablename__ = 'Biblioteca'

    idBiblioteca = Column(Integer, primary_key=True, autoincrement=True)
    idUsuario = Column(Integer)
    idObras = Column(Integer)