from App.dapendencias.config import Settings
from sqlalchemy import Integer, String, Column


class UsuarioModel(Settings.DBBaseModel):
    __tablename__ = 'Usuario'

    idUsuario= Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256))
    endereco = Column(String(256))
    telefone = Column(Integer)
    cpf = Column(Integer)
    grupo = Column(String(256))