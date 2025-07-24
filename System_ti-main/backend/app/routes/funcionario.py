from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import sessionmaker, relationship
from ..models.funcionario import Funcionario as FuncionarioModel
from ..models.setor import Setor
from ..models.sistema import Sistema as SistemaModel
from ..models.grupo_email import GrupoEmail
from ..schemas.funcionario import FuncionarioCreate, Funcionario as FuncionarioSchema
from ..schemas.sistema import Sistema as SistemaSchema
from ..schemas.setor import SetorOut
from ..schemas.grupo_email import GrupoEmailOut
from ..database import engine

router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@router.post('/funcionarios/', response_model=FuncionarioSchema)
def adicionar_funcionario(funcionario: FuncionarioCreate):
    db = SessionLocal()
    novo_funcionario = FuncionarioModel(
        nome=funcionario.nome,
        sobrenome=funcionario.sobrenome,
        cargo=funcionario.cargo,
        celular=funcionario.celular,
        email=funcionario.email
    )
    db.add(novo_funcionario)
    db.commit()
    db.refresh(novo_funcionario)
    # Vincula setores
    if funcionario.setores_ids:
        setores = db.query(Setor).filter(Setor.id.in_(funcionario.setores_ids)).all()
        novo_funcionario.setores = setores
    # Vincula sistemas
    if funcionario.sistemas_ids:
        sistemas = db.query(SistemaModel).filter(SistemaModel.id.in_(funcionario.sistemas_ids)).all()
        novo_funcionario.sistemas = sistemas
    # Vincula grupos de e-mail
    if funcionario.grupos_email_ids:
        grupos = db.query(GrupoEmail).filter(GrupoEmail.id.in_(funcionario.grupos_email_ids)).all()
        novo_funcionario.grupos_email = grupos
    db.commit()
    funcionario_schema = FuncionarioSchema.from_orm(novo_funcionario)
    funcionario_schema.setores = [SetorOut.from_orm(setor) for setor in novo_funcionario.setores]
    funcionario_schema.sistemas = [SistemaSchema.from_orm(sistema) for sistema in novo_funcionario.sistemas]
    funcionario_schema.grupos_email = [GrupoEmailOut.from_orm(grupo) for grupo in novo_funcionario.grupos_email]
    db.close()
    return funcionario_schema

@router.get('/funcionarios/{id}/sistemas', response_model=list[SistemaSchema])
def get_funcionario_sistemas(id: int):
    db = SessionLocal()
    funcionario = db.query(FuncionarioModel).filter(FuncionarioModel.id == id).first()
    if funcionario:
        sistemas = funcionario.sistemas
    else:
        sistemas = []
    db.close()
    return sistemas

@router.get('/funcionarios/', response_model=list[FuncionarioSchema])
def list_funcionarios():
    db = SessionLocal()
    funcionarios = db.query(FuncionarioModel).all()
    resultado = []
    for funcionario in funcionarios:
        setores = [SetorOut.from_orm(setor) for setor in funcionario.setores]
        sistemas = [SistemaSchema.from_orm(sistema) for sistema in funcionario.sistemas]
        grupos_email = [GrupoEmailOut.from_orm(grupo) for grupo in funcionario.grupos_email]
        funcionario_schema = FuncionarioSchema.model_validate({
            **funcionario.__dict__,
            'setores': setores,
            'sistemas': sistemas,
            'grupos_email': grupos_email
        })
        resultado.append(funcionario_schema)
    db.close()
    return resultado

@router.put('/funcionarios/{id}', response_model=FuncionarioSchema)
def atualizar_funcionario(id: int, funcionario: FuncionarioCreate):
    db = SessionLocal()
    db_funcionario = db.query(FuncionarioModel).filter(FuncionarioModel.id == id).first()
    if not db_funcionario:
        db.close()
        raise HTTPException(status_code=404, detail='Funcionário não encontrado')
    db_funcionario.nome = funcionario.nome
    db_funcionario.sobrenome = funcionario.sobrenome
    db_funcionario.cargo = funcionario.cargo
    db_funcionario.celular = funcionario.celular
    db_funcionario.email = funcionario.email
    # Atualiza grupos de e-mail
    if funcionario.grupos_email_ids:
        grupos = db.query(GrupoEmail).filter(GrupoEmail.id.in_(funcionario.grupos_email_ids)).all()
        db_funcionario.grupos_email = grupos
    else:
        db_funcionario.grupos_email = []
    # Atualiza setores
    if funcionario.setores_ids:
        setores = db.query(Setor).filter(Setor.id.in_(funcionario.setores_ids)).all()
        db_funcionario.setores = setores
    else:
        db_funcionario.setores = []
    # Atualiza sistemas
    if funcionario.sistemas_ids:
        sistemas = db.query(SistemaModel).filter(SistemaModel.id.in_(funcionario.sistemas_ids)).all()
        db_funcionario.sistemas = sistemas
    else:
        db_funcionario.sistemas = []
    db.commit()
    db.refresh(db_funcionario)
    funcionario_schema = FuncionarioSchema.from_orm(db_funcionario)
    funcionario_schema.setores = [SetorOut.from_orm(setor) for setor in db_funcionario.setores]
    funcionario_schema.sistemas = [SistemaSchema.from_orm(sistema) for sistema in db_funcionario.sistemas]
    db.close()
    return funcionario_schema

@router.delete('/funcionarios/{id}')
def excluir_funcionario(id: int):
    db = SessionLocal()
    db_funcionario = db.query(FuncionarioModel).filter(FuncionarioModel.id == id).first()
    if not db_funcionario:
        db.close()
        raise HTTPException(status_code=404, detail='Funcionário não encontrado')
    db.delete(db_funcionario)
    db.commit()
    db.close()
    return {'ok': True}

