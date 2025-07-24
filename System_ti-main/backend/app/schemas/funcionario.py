
from typing import List
from pydantic import BaseModel
from app.schemas.sistema import Sistema
from app.schemas.setor import SetorOut
from app.schemas.grupo_email import GrupoEmailOut

class FuncionarioBase(BaseModel):
    nome: str
    sobrenome: str
    setores_ids: List[int] = []
    sistemas_ids: List[int] = []
    grupos_email_ids: List[int] = []
    celular: str
    cargo: str = ''
    email: str

class FuncionarioCreate(FuncionarioBase):
    pass

class Funcionario(FuncionarioBase):
    id: int
    setores: List[SetorOut] = []
    sistemas: List[Sistema] = []
    grupos_email: List[GrupoEmailOut] = []
    class Config:
        orm_mode = True
        from_attributes = True
