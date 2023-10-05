from App.dapendencias.config import Settings
from sqlalchemy import Integer, String, Column


class HistoricoEmprestimosModel(Settings.DBBaseModel):
    __tablename__ = 'HistoricoEmprestimos'

    idEmprestimo = Column(Integer, primary_key=True, autoincrement=True)
    idUsuario = Column(Integer)
    idObras = Column(Integer)
    idCategoria = Column(Integer)
    idEditora = Column(Integer)
    idEmprestimo = Column(Integer)
    dataEmprestimos = Column(String(256))
    dataDevolucao = Column(String(256))
    status = Column(String(256))