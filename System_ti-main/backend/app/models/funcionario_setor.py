from app.models.base import Base
from sqlalchemy import Column, Integer, ForeignKey

class FuncionarioSetor(Base):
    __tablename__ = 'funcionario_setores'
    funcionario_id = Column(Integer, ForeignKey('funcionarios.id'), primary_key=True)
    setor_id = Column(Integer, ForeignKey('setores.id'), primary_key=True)
